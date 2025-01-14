import requests

class RuckusClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.headers.update({"Content-Type": "application/json"})

    def get_zones(self):
        url = f"{self.base_url}/rkszones"
        response = self.session.get(url, verify=False)  # Desactiva la verificación SSL si es necesario
        if response.status_code == 200:
            return response.json().get("rkszones", [])
        else:
            response.raise_for_status()


