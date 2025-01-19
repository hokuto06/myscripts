from netmiko import ConnectHandler
import re
# Configuración del dispositivo Cisco
device = {
    'device_type': 'cisco_ios',  # Cambia esto si usas otro sistema operativo (e.g., nxos para Nexus)
    'host': '192.168.188.31',      # IP del switch
    'username': 'n1mbu5',         # Usuario SSH
    'password': 'n3tw0rks',      # Contraseña SSH
    'secret': 'n3tw0rks', # Contraseña enable, si aplica
}

try:
    # Conexión al dispositivo
    connection = ConnectHandler(**device)
    connection.enable()  # Entrar al modo enable, si es necesario

    # Ejecutar el comando 'show lldp neighbors'
    output = connection.send_command('show lldp neighbors')
    print("LLDP Neighbors:\n")
    # print(output)
    results = []
    for line in output.splitlines():
        # Buscar líneas que contengan Device ID, Local Interface y Port ID
        match = re.match(r'(\S+)\s+(\S+)\s+\d+\s+\S+\s+([\da-f\.]+)', line)
        if match:
            device_id, local_intf, port_id = match.groups()
            # Transformar MAC address al formato estándar
            mac_address = port_id.replace('.', '').upper()
            mac_address = ':'.join(mac_address[i:i+2] for i in range(0, len(mac_address), 2))
            results.append((device_id, local_intf, mac_address))

    # Mostrar los resultados procesados
    print("Device ID    Local Interface    MAC Address")
    for device_id, local_intf, mac_address in results:
        print(f"{device_id:<12} {local_intf:<16} {mac_address}")
    # print()
    # Cerrar la conexión
    connection.disconnect()

except Exception as e:
    print(f"Error: {e}")