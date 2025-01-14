import RuckusVirtualSmartZoneAPIClient
import json
from pprint import pprint
from datetime import datetime



class connectVsz():
    def __init__(self, vsz_ip):
        self.current_time = datetime.now()
        try:
            client = RuckusVirtualSmartZoneAPIClient.Client()
            client.connect(url='https://'+vsz_ip+':8443', username='admin', password='elrbsestNF!25')
            # client.connect(url='https://192.168.188.10:8443', username='admin', password='elrbsestNF!25')
            self.client = client
            # print(dir(self.client))
            # self.mac_address = mac_address
            self.status = 1
            # self.zones = get_zones()
            # zones = self.client.get(method='/rkszones')
            # zones_response = zones.json()
            # print(zones_response)
            # self.zones_dict = {zone["id"]: zone["name"] for zone in zones_response["list"]}
            # print(self.zones_dict)
            # print(self.zones_dict['e77fed82-1968-467c-9f82-57d41d51f0fb'])
            # self.apgroups = {}
            # # Iterar sobre cada zona
            # for id in zones_response["list"]:
            #     if self.zones_dict[id["id"]] != "Staging Zone":  # Excluir "Staging Zone"
            #         _id = id["id"]
                    
            #         # Consultar los grupos de la zona
            #         groups = self.client.get(method='/rkszones/'+_id+'/apgroups')
            #         groups_response = groups.json()
                    
            #         # Actualizar el diccionario de grupos para esta zona
            #         for group in groups_response["list"]:
            #             self.apgroups[group["id"]] = group["name"]  # Guardar grupo en apgroups

            # print(self.apgroups)
        except Exception as e:
            print(e)
 
    # response = client.get(method='/rkszones')
    # print(json.dumps(response.json(), indent=4))
 
    # response = client.get(method='/rkszones/28b9296d-7dc9-44d9-9221-80a926f1f4a0')
    # response = client.get(method='/rkszones/28b9296d-7dc9-44d9-9221-80a926f1f4a0/apgroups/4066127f-a6ed-4a26-8951-dab89c95d216')
 
    #cambia nombre de dispositivo.
 
    # def get_zones(self):
    #     zones = self.client.get(method='/rkszones')
    #     #/e77fed82-1968-467c-9f82-57d41d51f0fb/apgroups
    #     # zone_data = [{"zoneId": zone["id"], "zoneName": zone["name"]} for zone in zones["list"]]
    #     # print(zone_data)
    #     zones_response = json.dumps(zones.json(), indent=4)
    #     zones_dict = {zone["id"]: zone["name"] for zone in zones_response["list"]}
    #     return zones_dict


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

    def config_full_ap(self,mac_address,hostname, ip_address, ap_netmask, ap_gateway, description):
        # response = {"name":hostname,"descripcion":description,"mac_address":mac_address,"network":{"ip":ip_address}}
        print('mac address: '+mac_address)
        print('ip address: '+ip_address)
 
        response = self.client.put(method=f'/aps/'+mac_address, data={ "name":hostname
                                                                    #   "description":description,
                                                                    #   "network":{
                                                                    #     "ipType": "Static",
                                                                    #     "ip": ip_address,
                                                                    #     "netmask": ap_netmask,
                                                                    #     "gateway": ap_gateway,
                                                                    #     "primaryDns": ap_gateway
                                                                    #   }                                                               
                                                                })
        print(response)

    def config_ap(self,mac_address,hostname, ip_address, description):
        # response = {"name":hostname,"descripcion":description,"mac_address":mac_address,"network":{"ip":ip_address}}
        print('mac address: '+mac_address)
        print('ip address: '+ip_address)
 
        response = self.client.put(method=f'/aps/'+mac_address, data={ "name":hostname,
                                                                      "description":description,
                                                                      "network":{
                                                                        "ipType": "Static",
                                                                        "ip": ip_address,
                                                                        "netmask": "255.255.252.0",
                                                                        "gateway": "192.168.188.1",
                                                                        "primaryDns": "192.168.188.1"
                                                                      },
                                                                        "apMgmtVlan": {
                                                                            "id": 100,
                                                                            "mode": "USER_DEFINED"
                                                                         }
                                                                })
        print(response)
        # results = (json.dumps(response.json(), indent=4))
        # print(results)
 
    def desconnect(self):
        self.client.disconnect()