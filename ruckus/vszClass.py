import RuckusVirtualSmartZoneAPIClient
import json
from pprint import pprint
from datetime import datetime



class connectVsz():
    def __init__(self, ipController, userController='admin', passwordController='elrbsestNF!25'):
        self.current_time = datetime.now()
        try:
            client = RuckusVirtualSmartZoneAPIClient.Client()
            client.connect(url='https://'+ipController+':8443', username=userController, password=passwordController)
            self.client = client
            self.status = 1
        except Exception as e:
            print(e)

 
    def get_zones(self):
        zones = self.client.get(method='/rkszones')
        #/e77fed82-1968-467c-9f82-57d41d51f0fb/apgroups
        # zone_data = [{"zoneId": zone["id"], "zoneName": zone["name"]} for zone in zones["list"]]
        # print(zone_data)
        zones_response = json.dumps(zones.json(), indent=4)
        zones_dict = {zone["id"]: zone["name"] for zone in zones_response["list"]}
        return zones_dict

    def get_ap_info(self, mac_address):
        response = self.client.get(method='/aps/'+mac_address)
        if response.status_code == 200:
            results = (json.dumps(response.json(), indent=4))
            return results
 
 
    def search_ap(self,mac_address):
        response = self.client.get(method='/aps/'+mac_address)
        # print(response.status_code) # --> 204
        if response.status_code == 200:
            return('ok')
        else:
            return('no')
    def get_all_devices_single(self):
        # response = self.client.get(method='/aps/', data={'zone_id': 'a92aa2ff-de24-4ef8-aa54-8a672af846e2'})
        response = self.client.get(method='/aps/')
        if response.status_code == 200:
            results = (response.json())
            list_devices = []
            return results

    def get_all_devices(self, apGroup):
        response = self.client.get(method='/aps/')
        if response.status_code == 200:
            results = (response.json())
            list_devices = []
            for ap in results['list']:
                json_info_ap = self.client.get(method='/aps/'+ap['mac'])
                info_ap = (json_info_ap.json())
                list_devices.append({"mac":ap['mac'],
                                    "name":info_ap.get('name','none'),
                                    "model":info_ap['model'],
                                    "serial":info_ap['serial'],
                                    "zoneId":ap['zoneId'],
                                    "apGroupId":ap['apGroupId'],
                                    "description":info_ap.get('description','none'),
                                    "ip_device": info_ap['network'].get('ip', 'None'),
                                    "lastConection":self.current_time,
                })
                print(list_devices)
            return list_devices
        

    def config_ap(self,mac_address, device_name=None, device_ip=None, device_netmask=None, device_gateway=None, device_dns=None, device_description=None):

        update_payload = {}
        
        if device_name:
            update_payload["name"] = device_name

        if device_description:
            update_payload["description"] = device_description

        if device_ip:
            if not (device_netmask and device_gateway and device_dns):
                print("Error: Para actualizar la IP, debes proporcionar la netmask, gateway y DNS.")
                return None
            print(mac_address, device_ip, device_netmask, device_gateway, device_dns)
            update_payload["network"] = {
                "ipType": "Static",
                "ip": device_ip,
                "netmask": device_netmask,
                "gateway": device_gateway,
                "primaryDns": device_dns
            }
            update_payload["apMgmtVlan"] = {
                "id": 100,
                "mode": "USER_DEFINED"
            }
        if not update_payload:
            print("Error: Debes proporcionar al menos un parámetro para actualizar (IP o nombre).")
            return None        
        pprint(update_payload)
        try:
            response = self.client.put(method='/aps/'+mac_address, data=update_payload)

        except Exception as e:
            print(f"Excepción durante la configuración del dispositivo: {e}")
            return None

        print(response) 

    def desconnect(self):
        self.client.disconnect()