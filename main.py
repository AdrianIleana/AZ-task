import requests
import yaml

tenant_id = "anu85007"
token = "9EeXSKQaRFCWKo9WbuUGd"
header_prefix = "Api-token"
URL = "https://{}.live.dynatrace.com/api/config/v1/managementZones".format(tenant_id)
header = {
    "Authorization": "{} {}".format(header_prefix, token),
    "Content-Type": "application/json"
}


def rule_gen(prefix):
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


def post_mz(new_data):
    response = requests.post(
        URL,
        json=new_data,
        headers=header
    )

    if response:
        print(f"Response status code is: {response.status_code}")
    else:
        print(f"""An error has occurred
            Response status code is: {response.status_code}""")


def get_mz():
    zones = dict()
    response = requests.get(
        URL,
        headers=header
    )
    if response:
        print(f"Response status code is: {response.status_code}")
        zones = response.json()
    else:
        print(f"""An error has occurred
            Response status code is: {response.status_code}""")
    return zones


def put_mz(new_data, mz_id):
    response = requests.put(
        URL + "/{}".format(mz_id),
        json=new_data,
        headers=header
    )

    if response.status_code:
        print(f"Response status code is: {response.status_code}")
    else:
        print(f"""An error has occurred
            Response status code is: {response.status_code}""")


def is_existing_mz(name, zones):
    for zone in zones:
        if zone['name'] == name:
            return zone
    return False


if __name__ == '__main__':
    file = open("input.yml")

    file_content = yaml.load(file, Loader=yaml.FullLoader)

    teams = file_content["teams"]

    mgmt_zones = get_mz()

    for title in teams.keys():
        payload = dict()
        payload["name"] = title
        if "host-group-prefixes" in teams[title].keys():
            list_of_rules = []
            for prefix in teams[title]["host-group-prefixes"]:
                rule = rule_gen(prefix)
                list_of_rules.append(rule)
            payload["rules"] = list_of_rules
        if is_existing_mz(title, mgmt_zones['values']):
            zone = is_existing_mz(title, mgmt_zones['values'])
            put_mz(payload, zone['id'])
        else:
            post_mz(payload)
