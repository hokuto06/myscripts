from netmiko import ConnectHandler
import re
from openpyxl import Workbook
device = {
    'device_type': 'cisco_ios',
    'host': '192.168.188.31',
    'username': 'n1mbu5',
    'password': 'n3tw0rks',
    'secret': 'n3tw0rks',
}
try:
    connection = ConnectHandler(**device)
    connection.enable()  
    prompt = connection.find_prompt()
    hostname = re.match(r"(\S+)[>#]", prompt).group(1)
    output = connection.send_command('show lldp neighbors')
    print("LLDP Neighbors:\n")
    results = []
    for line in output.splitlines():
        match = re.match(r'(\S+)\s+(\S+)\s+\d+\s+\S+\s+([\da-f\.]+)', line)
        if match:
            device_id, local_intf, port_id = match.groups()
            mac_address = port_id.replace('.', '').upper()
            mac_address = ':'.join(mac_address[i:i+2] for i in range(0, len(mac_address), 2))
            results.append((hostname,device_id, local_intf, mac_address))

    wb = Workbook()
    ws = wb.active
    ws.title = "SWITCHES"
    ws.append(["Switch Hostname", "MAC Address", "Interface", "Device Hostname"])
    for row in results:
        ws.append(row)
    wb.save("switches.xlsx")

    connection.disconnect()

except Exception as e:
    print(f"Error: {e}")