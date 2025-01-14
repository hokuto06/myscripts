# from unificontrol import UnifiClient
# from openpyxl import load_workbook

# def unifi_controller():
#     uc_user = "rsupport"
#     uc_pass = "elrbsestNF!25"
#     uc_site = "etw7f5dj"
#     client = UnifiClient(host="172.20.197.148",
#     username=uc_user, password=uc_pass, site=uc_site)
#     devices = client.adopt_device('78:45:58:ef:13:f1')
#     return 'ok'

# unifi_controller()

##########################################################################
##########################################################################
##########################################################################

import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from pprint import pprint
import pandas as pd

# Datos del controlador UniFi
controller_url = "https://172.20.197.148:8443/api/login"
username = "rsupport"
password = "elrbsestNF!25"
device_id = "66f8af48d51d7f60b1d50ac8"
new_ip = "192.168.222.101"  # Nueva IP estática que deseas asignar
new_name = "NuevoNombreAP"  # Nuevo nombre que deseas asignar al AP
controller_url_api = "https://172.20.197.148:8443/api/s/etw7f5dj"
# controller_url_api = "https://172.20.197.148:8443/api/s/x02q4578"

# Autenticación
login_url = f"{controller_url}login"
payload = {"username": username, "password": password}
session = requests.Session()
login_response = session.post(controller_url, headers={"Accept":"application/json","Content-Type":"application/json"}, data=json.dumps(payload), verify=False)
api_data = login_response.json()
pprint(api_data)

if login_response.status_code == 200:
    print("Autenticación exitosa")

    # Endpoint para modificar el dispositivo
#     update_device_url = f"{controller_url_api}/rest/device/{device_id}"

#     # Datos que deseas actualizar (nombre e IP)
#     update_payload = {
#         "name": new_name,           # Actualizar nombre
#         'config_network': {'dns1': '192.168.222.1',
#                             'gateway': '192.168.222.1',
#                             'ip': '192.168.222.101',
#                             'netmask': '255.255.255.0',
#                             'type': 'static'}
#     }

#     # Enviar la solicitud PUT para actualizar el dispositivo
#     response = session.put(update_device_url, json=update_payload, verify=False)

#     if response.status_code == 200:
#         print(f"El dispositivo {new_name} se actualizó con éxito.")
#     else:
#         print(f"Error al actualizar el dispositivo: {response.text}")
# else:
#     print("Error en la autenticación:", login_response.text)

devices_url = f"{controller_url_api}/stat/device"
response = session.get(devices_url, verify=False)
### excel




####
if response.status_code == 200:
    # devices = response.json()
    devices = json.loads(response.text)
    device_list = devices.get("data", [])    
    # pprint(dev    ices)    
    # Filtrar los campos requeridos
    # for device in device_list:
    #     device_id = device.get("_id", "N/A")
    #     mac_address = device.get("mac", "N/A")
    #     name = device.get("name", "N/A")
    #     model = device.get("model", "N/A")
    #     last_uplink = device.get("last_uplink", "N/A")
    #     if last_uplink != "N/A":
    #         uplink_port = last_uplink.get("uplink_remote_port", "N/A")
    #         uplink_mac = last_uplink.get("uplink_mac","N/A")
    #     ip_address = device.get("ip", "N/A")
    #     print(f"ID: {device_id}, MAC: {mac_address}, Name: {model}, uplink_mac: {uplink_mac},uplink_port: {uplink_port}, Name: {name}, IP: {ip_address}")
    # Supongamos que 'devices' es un diccionario con los datos
    devices_data = devices.get("data", [])  # Acceder a la lista de dispositivos

    # Extraer los campos que nos interesan y convertirlos en una lista de diccionarios
    rows = []
    for device in devices_data:
        last_uplink = device.get("last_uplink", "N/A")
        if last_uplink != "N/A":
            uplink_port = last_uplink.get("uplink_remote_port", "N/A")
            uplink_mac = last_uplink.get("uplink_mac","N/A")
        rows.append({

        "ID" : device.get("_id", "N/A"),
        "MAC" : device.get("mac", "N/A"),
        "NAME" : device.get("name", "N/A"),
        "MODEL" : device.get("model", "N/A"),
        "IP" : device.get("ip", "N/A"),
        "UPLINK MAC" : last_uplink.get("uplink_mac", "N/A"),
        "UPLINK PORT" : last_uplink.get("uplink_remote_port", "N/A"),
        "TYPE" : device.get("type", "N/A"),
            # "ID": device.get("_id", "N/A"),
            # "MAC Address": device.get("mac", "N/A"),
            # "Name": device.get("name", "N/A"),
            # "IP Address": device.get("ip", "N/A"),
        })

    # Crear un DataFrame con pandas
    df = pd.DataFrame(rows)

    # Guardar el DataFrame en un archivo Excel
    output_file = "devices_output.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Archivo guardado como {output_file}")
else:
    print("Error al obtener dispositivos:", response.status_code, response.text)