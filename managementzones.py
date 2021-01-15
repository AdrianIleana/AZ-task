import yaml
import requests
from requests import HTTPError


class ManagementZones:
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
        try:
            response = requests.get(
                self.URL,
                headers=self.header
            )
            if response.status_code == 200:
                print(f"\nGET request status code is: {response.status_code}")
                zones = response.json()
                print(f"GET retrieved {len(zones['values'])} existing zones.\n")
            else:
                print(f"""An error has occurred
                    Response status code is: {response.status_code}""")
            return zones
        except requests.ConnectionError as e:
            print(f"Error encountered {e}")

    def post_mz(self, new_data):
        url_validator = self.URL + "/validator"

        try:
            response_validator = requests.post(
                url_validator,
                json=new_data,
                headers=self.header
            )

            # Raise HTTP exception if validator check fails:
            response_validator.raise_for_status()

            if response_validator.status_code == 204:
                post_req = requests.post(
                    self.URL,
                    json=new_data,
                    headers=self.header
                )
                print(f"\nPOST request ran with response code: {post_req.status_code}")
                print(f"POST request successfully created new management zone: {new_data['name']}")
        except HTTPError:
            print(f"PUT failed with HTTPError: {response_validator.content}\n")
        except Exception as e:
            print(f"PUT failed with exception: {e} \n")

    def put_mz(self, new_data, mz_id):
        url_validator = self.URL + "/{}/validator".format(mz_id)

        try:
            response_validator = requests.post(
                url_validator,
                json=new_data,
                headers=self.header
            )

            # Raise HTTP exception if validator check failed:
            response_validator.raise_for_status()

            if response_validator.status_code == 204:
                put_req = requests.put(
                    self.URL + "/{}".format(mz_id),
                    json=new_data,
                    headers=self.header
                )
                print(f"\nPUT request ran with response code: {put_req.status_code}")
                print(f"PUT request successfully updated management zone: {new_data['name']}")
        except HTTPError:
            print(f"PUT failed with HTTPError: {response_validator.content}\n")
        except Exception as e:
            print(f"PUT failed with exception: {e} \n")

    def exists_in(self, name, zones):
        for zone in zones:
            if zone['name'] == name:
                return zone
        return False

    def rule_gen(self, prefix):
        rule = {
           "type": "PROCESS_GROUP",
           "enabled": True,
           "propagationTypes": [
              "PROCESS_GROUP_TO_SERVICE",
              "PROCESS_GROUP_TO_HOST"
           ],
           "conditions": [
              {
                 "key": {
                    "attribute": "HOST_GROUP_NAME"
                 },
                 "comparisonInfo": dict(type="STRING", operator="BEGINS_WITH", value=prefix, negate=False,
                                        caseSensitive=True)
              }
           ]
        }
        return rule
