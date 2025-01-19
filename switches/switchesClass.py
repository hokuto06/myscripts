# Clase base para switches
import re
from netmiko import ConnectHandler

class Switch:
    def __init__(self, ip, username, password, device_type):
        self.ip = ip
        self.username = username
        self.password = password
        self.device_type = device_type
        self.connection = None
        self.hostname = None

    def connect(self):
        self.connection = ConnectHandler(
            device_type=self.device_type,
            host=self.ip,
            username=self.username,
            password=self.password,
            secret=self.password,
        )
        self.connection.enable()
        self.hostname = re.match(r"(\S+)[>#]", self.connection.find_prompt()).group(1)

    def disconnect(self):
        if self.connection:
            self.connection.disconnect()

    def get_neighbors(self):
        raise NotImplementedError("Subclasses should implement this method.")


class CiscoSwitch(Switch):
    def __init__(self, ip, username, password):
        super().__init__(ip, username, password, "cisco_ios")

    def get_neighbors(self):
        output = self.connection.send_command('show lldp neighbors')
        data = []
        for line in output.splitlines():
            match = re.match(r'(\S+)\s+(\S+)\s+\d+\s+\S+\s+([\da-f\.]+)', line)
            if match:
                device_id, local_intf, port_id = match.groups()
                mac_address = port_id.replace('.', '').upper()
                mac_address = ':'.join(mac_address[i:i+2] for i in range(0, len(mac_address), 2))
                data.append([self.hostname, mac_address, local_intf, device_id])
        return data


class ArubaSwitch(Switch):
    def __init__(self, ip, username, password):
        super().__init__(ip, username, password, "aruba_os")

    def connect(self):
        self.connection = ConnectHandler(
            device_type=self.device_type,
            host=self.ip,
            username=self.username,
            password=self.password,
            global_delay_factor=2  # Aumentar tiempo entre comandos
        )
        # Leer el banner completo y manejar "Press any key to continue"
        output = self.connection.read_channel()
        if "Press any key to continue" in output:
            self.connection.write_channel("\n")
            self.connection.read_until_prompt()

        self.connection.enable()
        self.hostname = re.match(r"(\S+)[>#]", self.connection.find_prompt()).group(1)

    def get_neighbors(self):
        output = self.connection.send_command('sh lldp info remote-device')
        data = []
        for line in output.splitlines():
            match = re.match(r'\s*(\d+)\s+\|\s+([\da-f\s]+)\s+([\da-f\s]+)\s+\S+\s+(\S+)?', line)
            if match:
                local_port, chassis_id, port_id, sys_name = match.groups()
                mac_address = chassis_id.replace(' ', '').upper()
                mac_address = ':'.join(mac_address[i:i+2] for i in range(0, len(mac_address), 2))
                sys_name = sys_name if sys_name else "Unknown"
                data.append([self.hostname, mac_address, f"Port {local_port}", sys_name])
        return data


class BrocadeSwitch(Switch):
    def __init__(self, ip, username, password):
        super().__init__(ip, username, password, "brocade_fastiron")

    def get_neighbors(self):
        hostname = self.hostname.split('@')
        output = self.connection.send_command('show lldp neighbors')
        data = []
        for line in output.splitlines():
            match = re.match(r'(\S+)\s+([\da-f\.]+)\s+([\da-f\.]+)\s+\S+\s+(\S+)', line)
            if match:
                local_port, chassis_id, port_id, sys_name = match.groups()
                mac_address = chassis_id.replace('.', '').upper()
                mac_address = ':'.join(mac_address[i:i+2] for i in range(0, len(mac_address), 2))
                data.append([hostname[1], mac_address, local_port, sys_name])
        return data


