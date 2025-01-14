import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from pprint import pprint

class UnifiApiController:

    def __init__(self, ipController="172.20.197.148", port="8443", userController="rsupport", passwordController="elrbsestNF!25" ):
        controller_url = "https://"+ipController+":"+port+"/api/login"
        self.controller_url = controller_url
        self.controller_url_api = "https://"+ipController+":"+port+"/api/s/default"
        payload = {"username": userController, "password": passwordController}
        self.session = requests.Session()
        login_response = self.session.post(controller_url, headers={"Accept":"application/json","Content-Type":"application/json"}, data=json.dumps(payload), verify=False)
        api_data = login_response.json()
        pprint(api_data)

        if login_response.status_code == 200:
            print("Autenticación exitosa")
        else:
            print("Error en la autenticación:", login_response.text)

    def getDevices(self):
        # if response.status_code == 200:
        devices_url = f"{self.controller_url_api}/stat/device"
        response = self.session.get(devices_url, verify=False)            
        devices = json.loads(response.text)
        devices_data = devices.get("data", [])  # Acceder a la lista de dispositivos
        rows = []
        for device in devices_data:
            last_uplink = device.get("last_uplink", {})
            uplink_mac = last_uplink.get("uplink_mac", "N/A")
            uplink_port = last_uplink.get("uplink_remote_port", "N/A")
            
            rows.append({
                "ID": device.get("_id", "N/A"),
                "MAC": device.get("mac", "N/A"),
                "NAME": device.get("name", "N/A"),
                "MODEL": device.get("model", "N/A"),
                "IP": device.get("ip", "N/A"),
                "UPLINK MAC": uplink_mac,
                "UPLINK PORT": uplink_port,
                "TYPE": device.get("type", "N/A"),
            })
        return rows

    def setupDevice(self, device_id, device_ip=None, device_name=None, device_netmask=None, device_gateway=None, device_dns=None): 

        update_device_url = f"{self.controller_url_api}/rest/device/{device_id}"

        update_payload = {}
        
        if device_name:
            update_payload["name"] = device_name

        if device_ip:
            if not (device_netmask and device_gateway and device_dns):
                print("Error: Para actualizar la IP, debes proporcionar la netmask, gateway y DNS.")
                return None
            update_payload["config_network"] = {
                "type": "static",
                "ip": device_ip,
                "netmask": device_netmask,
                "gateway": device_gateway,
                "dns1": device_dns
            }

        if not update_payload:
            print("Error: Debes proporcionar al menos un parámetro para actualizar (IP o nombre).")
            return None

        try:
            response = self.session.put(update_device_url, json=update_payload, verify=False)

            if response.status_code == 200:
                print(f"El dispositivo se actualizó con éxito: {update_payload}")
                return response.json() 
            else:
                print(f"Error al actualizar el dispositivo {device_id}: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Excepción durante la configuración del dispositivo: {e}")
            return None

    def setDeviceTag(self):
        site_id = "64c08dd9d51d7f0296e44f5f"

        # Endpoint para crear un nuevo tag
        tag_url = f"{self.controller_url_api}/api/s/{site_id}/rest/tag/676ad32fd952beccefd85977"

        # Crear el payload para el nuevo tag
        payload = {
            # "name": "test",
            "site_id":site_id,
            "member_table": ["60:22:32:1e:e0:27"]  # Asignar la MAC al crear el tag
        }

        # Enviar solicitud POST para crear el tag
        response = self.session.post(tag_url, json=payload, verify=False)

        if response.status_code == 200:
            tag_data = response.json()
            print(f"Tag creado correctamente con la MAC .")
            print(f"ID del Tag: {tag_data.get('_id', 'No disponible')}")
        else:
            print(f"Error al crear el tag: {response.status_code} - {response.text}")


    def get_tags(self):
        # Endpoint para obtener los tags del sitio default
        tags_url = f"{self.controller_url_api}/rest/tag"

        try:
            # Realizar una solicitud GET para obtener los tags
            response = self.session.get(tags_url, verify=False)

            if response.status_code == 200:
                tags_data = response.json().get("data", [])  # Obtener los datos de los tags

                tags_info = []
                for tag in tags_data:
                    tags_info.append({
                        "ID": tag.get("_id", "N/A"),
                        "Name": tag.get("name", "N/A"),
                        "MACs": tag.get("member_table", [])  # Lista de MACs asociadas al tag
                    })

                pprint(tags_info)
                return tags_info
            else:
                print(f"Error al obtener los tags: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Excepción al obtener los tags: {e}")
            return None
