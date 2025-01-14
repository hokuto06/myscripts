# Uso del cliente
from myvszApi import RuckusClient

vsz_client = RuckusClient("http://192.168.188.10", "admin", "elrbsestNF!25")
zones = vsz_client.get_zones()

for zone in zones:
    print(f"Zone ID: {zone['id']}, Zone Name: {zone['name']}")