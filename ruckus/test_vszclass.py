from vszClass import connectVsz

controller = connectVsz('192.168.188.10')
controller.config_ap("3C:46:A1:2B:14:70",device_ip="192.168.112.199", device_netmask="255.255.252.0",device_dns="192.168.112.1",device_gateway="192.168.112.1" )


# import RuckusVirtualSmartZoneAPIClient
# from pprint import pprint

# client = RuckusVirtualSmartZoneAPIClient.Client()
# client.connect(url='https://192.168.188.10:8443', username='admin', password='elrbsestNF!25')
# payload = {}
# payload['network'] = {
#                                                                         "ipType": "Static",
#                                                                         "ip": "192.168.112.198",
#                                                                         "netmask": "255.255.252.0",
#                                                                         "gateway": "192.168.112.1",
#                                                                         "primaryDns": "192.168.112.1"
#                                                                       }
                                                                

# pprint(payload)
# response = client.put(method=f'/aps/3C:46:A1:2B:14:70', data=payload)

# print(response)