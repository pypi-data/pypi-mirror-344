#!/usr/bin/env python3
# encoding:utf-8


import collections
import hashlib
import re
import subprocess
from configparser import ConfigParser
from contextlib import ExitStack
from datetime import datetime
from io import StringIO
from ipaddress import ip_address, ip_network, IPv4Address, IPv4Network, IPv6Address, IPv6Network
from pathlib import Path
from subprocess import STDOUT
from threading import get_ident
from typing import Dict, FrozenSet, Tuple

from cryptography.utils import cached_property
from parallel_utils.thread import create_thread

from wirescale.communications.common import BytesStrConverter, CONNECTION_PAIRS, file_locker, subprocess_run_tmpfile
from wirescale.communications.messages import ActionCodes, ErrorMessages, Messages
from wirescale.communications.systemd import Systemd
from wirescale.vpn.exit_node import ExitNode
from wirescale.vpn.iptables import IPTABLES
from wirescale.vpn.tsmanager import TSManager


class WGConfig:
    repeatable_fields = frozenset(('address', 'dns', 'preup', 'postup', 'predown', 'postdown', 'allowedips'))
    configfile = Path('/run/wirescale/%i.conf')

    def __init__(self, file_path: Path):
        self.file_path: Path = file_path
        self.config: ConfigParser = ConfigParser(interpolation=None)
        self.config.optionxform = lambda option: option
        self.counters: Dict = {}
        self.read_config()
        self.addresses = self.get_addresses()
        self.allow_suffix: bool = self.get_wirescale_field(field='suffix', func=self.config.getboolean)
        self.expected_interface: str = None
        self.remote_addresses: FrozenSet[IPv4Address | IPv6Address] = None
        self.private_key = self.get_field('Interface', 'PrivateKey') or self.generate_wg_privkey()
        self.listen_port = TSManager.local_port()
        self.listen_ext_port: int = None
        self.endpoint: Tuple[IPv4Address, int] = None
        self.exit_node: bool = False
        self.table = table.lower() if (table := self.get_field('Interface', 'Table')) else None
        self.mtu = self.get_field('Interface', 'MTU')
        self.nat: bool = None
        self.fwmark = self.get_field('Interface', 'FwMark')
        self.allowed_ips = self.get_allowed_ips()
        self.interface: str = self.get_wirescale_field(field='interface')
        self.iptables_accept: bool = self.get_wirescale_field(field='iptables-accept', func=self.config.getboolean)
        self.iptables_forward: bool = self.get_wirescale_field(field='iptables-forward', func=self.config.getboolean)
        self.iptables_masquerade: bool = self.get_wirescale_field(field='iptables-masquerade', func=self.config.getboolean)
        self.public_key = self.generate_wg_pubkey(self.private_key)
        self.recover_tries: int = self.get_wirescale_field(field='recover-tries', func=self.config.getint)
        self.recreate_tries: int = self.get_wirescale_field(field='recreate-tries', func=self.config.getint)
        self.remote_interface: str = None
        self.remote_local_port: int = None
        self.remote_pubkey: str = self.get_field('Peer', 'PublicKey')
        self.psk = self.get_field('Peer', 'PresharedKey')
        self.has_psk: bool = self.psk is not None
        self.psk = self.psk or self.generate_wg_psk()
        self.start_time: int = datetime.now().second
        self.suffix: int = None

    @cached_property
    def mark(self) -> int:
        encoded_interface = BytesStrConverter.str_to_bytes(self.interface)
        hash_sha384 = hashlib.sha384(encoded_interface).hexdigest()
        return int(hash_sha384[:8], 16)  # return the first 32 bits

    def read_config(self):
        with open(self.file_path, 'r') as f:
            text = f.read()
        for field in self.repeatable_fields:
            field = field.lower()
            suffix = [1]  # We use a list so that the value is preserved between calls to the replace function

            def replace(match):
                old_str = match.group(0)
                result = f'{old_str}{suffix[0]}_'
                suffix[0] += 1
                return result

            text = re.sub(field, replace, text, flags=re.IGNORECASE)
            self.counters[field] = suffix[0] - 1
        self.config.read_string(text)

    def get_field(self, section_name: str, field: str, missing_section_ok=False) -> str | Tuple[str, ...] | None:
        field = field.lower()
        try:
            section = next(section for section in self.config.sections() if section.lower() == section_name.lower())
        except StopIteration as e:
            if missing_section_ok:
                return
            raise e
        if field not in self.repeatable_fields:
            return next((value for (name, value) in self.config.items(section) if name.lower() == field), None)
        return tuple(value for (name, value) in self.config.items(section) if name.lower().startswith(field))

    def get_addresses(self) -> FrozenSet[IPv4Address | IPv6Address] | None:
        lines: Tuple[str, ...] = self.get_field('interface', 'address')
        if not lines:
            return None
        return frozenset(ip_address(addr.strip()) for line in lines for addr in line.replace(',', ' ').split())

    def get_allowed_ips(self) -> FrozenSet[IPv4Network | IPv6Network] | None:
        lines: Tuple[str, ...] = self.get_field('peer', 'allowedips')
        if not lines:
            return None
        return frozenset(ip_network(addr.strip(), strict=False) for line in lines for addr in line.replace(',', ' ').split())

    def ip_is_allowed(self, ip: IPv4Address | IPv6Address) -> bool:
        return next((True for network in self.allowed_ips if ip in network), False)

    def add_script(self, action: str, script: str, first_place=False):
        interface = next(section for section in self.config.sections() if section.lower() == 'interface')
        if first_place:
            same_actions = [(name, value) for (name, value) in self.config.items(interface) if name.lower().startswith(action.lower())]
            collections.deque((self.config.remove_option(interface, name) for (name, _) in same_actions), maxlen=0)
        self.counters[action.lower()] += 1
        self.config.set(interface, f'{action}{self.counters[action.lower()]}_', script)
        if first_place:
            collections.deque((self.config.set(interface, name, value) for (name, value) in same_actions), maxlen=0)

    def add_iptables_accept(self):
        port = TSManager.local_port()
        postup_input_interface = IPTABLES.INPUT_ACCEPT_INTERFACE.format(interface=self.interface)
        postup_input_port = IPTABLES.INPUT_ACCEPT_PORT.format(port=port, interface=self.interface)
        postdown_input_interface = IPTABLES.or_true(IPTABLES.remove_rule(postup_input_interface))
        postdown_input_port = IPTABLES.or_true(IPTABLES.remove_rule(postup_input_port))
        self.add_script('postup', postup_input_interface)
        self.add_script('postup', postup_input_port)
        self.add_script('postdown', postdown_input_interface, first_place=True)
        self.add_script('postdown', postdown_input_port, first_place=True)

    def add_iptables_forward(self):
        postup_forward = IPTABLES.FORWARD.format(interface=self.interface)
        postup_forward_back = IPTABLES.FORWARD_BACK.format(interface=self.interface)
        postdown_forward = IPTABLES.or_true(IPTABLES.remove_rule(postup_forward))
        postdown_forward_back = IPTABLES.or_true(IPTABLES.remove_rule(postup_forward_back))
        self.add_script('postup', postup_forward_back)
        self.add_script('postup', postup_forward)
        self.add_script('postdown', postdown_forward_back, first_place=True)
        self.add_script('postdown', postdown_forward, first_place=True)
        subprocess.run(['sysctl', '-w', 'net.ipv4.ip_forward=1'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def add_iptables_masquerade(self):
        postup_mark = IPTABLES.FORWARD_MARK.format(mark=self.mark, interface=self.interface)
        postup_masquerade = IPTABLES.MASQUERADE.format(mark=self.mark, interface=self.interface)
        postdown_mark = IPTABLES.or_true(IPTABLES.remove_rule(postup_mark))
        postdown_masquerade = IPTABLES.or_true(IPTABLES.remove_rule(postup_masquerade))
        self.add_script('postup', postup_mark)
        self.add_script('postup', postup_masquerade)
        self.add_script('postdown', postdown_mark, first_place=True)
        self.add_script('postdown', postdown_masquerade, first_place=True)

    def first_handshake(self):
        handshake = (rf"""/bin/sh -c 'count=0; while [ $count -le 14 ]; do handshake=$(wg show %i latest-handshakes | awk -v pubkey="{self.remote_pubkey}" '\''$1 == pubkey {{print $2}}'\''); """
                     "if [ $handshake -eq 0 ]; then sleep 0.5; count=$((count+1)); else exit 0; fi; done; exit 1'")
        self.add_script('postup', handshake, first_place=True)

    def remove_exit_node(self):
        remove = rf"""/bin/sh -c '[ "$(wirescale exit-node --status)" = "{self.interface}" ] && wirescale exit-node --stop'"""
        wipe_allowed_ips = rf"""/bin/sh -c 'wg set {self.interface} peer {self.remote_pubkey} allowed-ips  ""'"""
        self.add_script('predown', f'{remove} || true')
        self.add_script('predown', wipe_allowed_ips)

    def sync_exit_node(self):
        sync = r"/bin/sh -c 'wirescale exit-node --sync'"
        self.add_script('postup', sync, first_place=True)
        self.add_script('postdown', sync)

    def autoremove_configfile(self):
        remove_configfile = f'rm -f {self.configfile}'
        self.add_script('postdown', remove_configfile, first_place=True)

    def set_metric(self, metric: int):
        metric = (r'/bin/bash -c "ip route | grep -w %i | while read -r line ; do ip route del $line; if [[ ${line##* } == metric ]]; then line=${line% *}; line=${line% *}; fi; '
                  fr'ip route add $line metric {metric}; done"')
        self.add_script('postup', metric, first_place=True)

    @staticmethod
    def generate_wg_privkey() -> str:
        return subprocess.run(['wg', 'genkey'], capture_output=True, text=True).stdout.strip()

    @staticmethod
    def generate_wg_pubkey(privkey: str) -> str:
        return subprocess.run(['wg', 'pubkey'], input=privkey, capture_output=True, text=True).stdout.strip()

    @classmethod
    def generate_wg_keypair(cls) -> Tuple[str, str]:
        private = cls.generate_wg_privkey()
        public = cls.generate_wg_pubkey(private)
        return private, public

    @staticmethod
    def generate_wg_psk() -> str:
        return subprocess.run(['wg', 'genpsk'], capture_output=True, text=True).stdout.strip()

    def generate_new_config(self):
        new_config = ConfigParser(interpolation=None)
        new_config.optionxform = lambda option: option
        interface, peer, allowedips = 'Interface', 'Peer', 'AllowedIPs'
        new_config.add_section(interface)
        new_config.add_section(peer)
        if self.iptables_accept:
            self.add_iptables_accept()
        if self.iptables_forward:
            self.add_iptables_forward()
        if self.iptables_masquerade:
            self.add_iptables_masquerade()
        self.remove_exit_node()
        self.sync_exit_node()
        # self.first_handshake()
        self.autoremove_configfile()
        repeatable_fields = [field for field in self.repeatable_fields if field != allowedips]
        for field in repeatable_fields:
            for i, value in enumerate(self.get_field(interface, field), start=1):
                new_config.set(interface, f'{field}{i}_', value)
        new_config.set(interface, 'ListenPort', str(self.listen_port))
        new_config.set(interface, 'PrivateKey', self.private_key)
        new_config.set(interface, 'MTU', self.mtu) if self.mtu else None
        new_config.set(interface, 'FwMark', self.fwmark) if self.fwmark else None
        new_config.set(peer, 'PublicKey', self.remote_pubkey)
        new_config.set(peer, 'PresharedKey', self.psk)
        new_config.set(peer, 'Endpoint', f'{self.endpoint[0]}:{self.endpoint[1]}')
        new_config.set(peer, 'PersistentKeepalive', '10')
        if self.table != 'off' and ExitNode.GLOBAL_NETWORK in self.allowed_ips:
            self.exit_node = True
            if len(self.allowed_ips) == 1:
                self.table = 'off'
            else:
                self.allowed_ips = set(self.allowed_ips)
                self.allowed_ips.remove(ExitNode.GLOBAL_NETWORK)
        new_config.set(interface, 'Table', self.table) if self.table else None
        new_config.set(peer, allowedips, ', '.join(str(x) for x in self.allowed_ips))
        new_config = self.write_config(new_config, self.suffix)
        self.new_config_path.write_text(new_config, encoding='utf-8')

    def get_wirescale_field(self, field, func=None):
        ws = 'Wirescale'
        section = next((section for section in self.config.sections() if section.lower() == ws.lower()), None)
        if section is None:
            return None
        value = self.get_field(section_name=section, field=field)
        if value is None or func is None:
            return value
        self.config.set(section=section, option=field, value=value)
        try:
            return func(section=section, option=field)
        except:
            pair = CONNECTION_PAIRS[get_ident()]
            error = ErrorMessages.BAD_WS_CONFIG.format(field=field, config_file=self.file_path)
            error_remote = ErrorMessages.REMOTE_BAD_WS_CONFIG.format(field=field, my_name=pair.my_name, my_ip=pair.my_ip, peer_name=pair.peer_name)
            ErrorMessages.send_error_message(local_message=error, remote_message=error_remote)

    @property
    def new_config_path(self):
        return Path('/run/wirescale/').joinpath(f'{self.interface}.conf')

    @classmethod
    def write_config(cls, config: ConfigParser, suffix: int = None):
        string_io = StringIO()
        config.write(string_io)
        text = string_io.getvalue()

        def replace(match):
            old_str = match.group(0)
            result = re.sub(r'\d+_', '', old_str, flags=re.IGNORECASE)
            return result

        for field in cls.repeatable_fields:
            text = re.sub(rf'{field}\d+_', replace, text, flags=re.IGNORECASE)

        if suffix is not None:
            text = text.replace('%s', str(suffix))

        return text

    def upgrade(self):
        from wirescale.communications.checkers import check_updated_handshake
        pair = CONNECTION_PAIRS[get_ident()]
        stack = ExitStack()
        stack.enter_context(file_locker())
        Messages.send_info_message(local_message='Stopping tailscale...')
        TSManager.stop()
        Messages.send_info_message(local_message=f"Setting up WireGuard interface '{self.interface}'...")
        wgquick = subprocess_run_tmpfile(['wg-quick', 'up', str(self.new_config_path)], stderr=STDOUT)
        Messages.send_info_message(local_message='Starting tailscale...')
        TSManager.start()
        create_thread(TSManager.wait_tailscale_restarted, pair, stack)
        if wgquick.returncode == 0:
            Messages.send_info_message(local_message='Verifying handshake with the other peer...')
            updated = check_updated_handshake(self.interface)
            if not updated:
                error = ErrorMessages.HANDSHAKE_FAILED.format(interface=self.interface)
                subprocess.run(['wg-quick', 'down', str(self.new_config_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                ErrorMessages.send_error_message(local_message=error)
            Systemd.launch_autoremove(config=self, pair=pair)
            if self.exit_node:
                ExitNode.modify_allowed_ips(self.interface)
                ExitNode.set_exit_node(self.interface)
            success = Messages.SUCCESS.format(interface=self.interface)
            Messages.send_info_message(local_message=success, code=ActionCodes.SUCCESS)
        else:
            self.new_config_path.unlink()
            final_error = '\n'.join(Messages.add_id(pair.id, m) for m in wgquick.stdout.strip().split('\n'))
            final_error = final_error.strip() + '\n' + Messages.add_id(pair.id, ErrorMessages.FINAL_ERROR)
            ErrorMessages.send_error_message(local_message=final_error)
