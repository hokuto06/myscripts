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
            global_delay_factor=2
        )
        # Manejo del mensaje inicial
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
            # Separar la línea por divisores (| o espacios dobles)
            parts = re.split(r'\s{2,}|\s+\|\s+', line.strip())
            if len(parts) >= 5:  # Asegurar que la línea tiene al menos los campos necesarios
                local_port = parts[0]
                port_id = parts[2].replace(' ', ':').upper()  # Convertir separador de espacios a ":"
                sys_name = parts[4] if len(parts) > 4 else "Unknown"
                data.append([self.hostname, port_id, local_port, sys_name])
        print(data)
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


