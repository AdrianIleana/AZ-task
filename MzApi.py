import yaml
import requests


class MzApi:
    def __init__(self, file):
        self.config = yaml.load(file, Loader=yaml.FullLoader)

        self.URL = "https://{}.live.dynatrace.com/api/config/v1/managementZones".format(self.config['tenant_id'])

        self.token = "9EeXSKQaRFCWKo9WbuUGd"

        self.header_prefix = "Api-token"

        self.header = {
            "Authorization": "{} {}".format(self.header_prefix, self.token),
            "Content-Type": "application/json"
        }

        self.Teams = self.config["teams"]

    def get_mz(self):
        zones = dict()
        response = requests.get(
            self.URL,
            headers=self.header
        )
        if response:
            print(f"Response status code is: {response.status_code}")
            zones = response.json()
        else:
            print(f"""An error has occurred
                Response status code is: {response.status_code}""")
        return zones

    def post_mz(self, new_data):
        response = requests.post(
            self.URL,
            json=new_data,
            headers=self.header
        )

        if response:
            print(f"Response status code is: {response.status_code}")
        else:
            print(f"""An error has occurred
                Response status code is: {response.status_code}""")

    def put_mz(self, new_data, mz_id):
        response = requests.put(
            self.URL + "/{}".format(mz_id),
            json=new_data,
            headers=self.header
        )

        if response.status_code:
            print(f"Response status code is: {response.status_code}")
        else:
            print(f"""An error has occurred
                Response status code is: {response.status_code}""")

    def is_existing_mz(self, name, zones):
        for zone in zones:
            if zone['name'] == name:
                return zone
        return False
