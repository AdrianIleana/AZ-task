from managementzones import ManagementZones
import yaml
import base64


# Function for decoding from Base64 format:
def token_decode(encoded_file):
    base64_bytes = encoded_file.read().encode('utf-8')
    text_to_bytes = base64.b64decode(base64_bytes)
    decoded = text_to_bytes.decode('utf-8')
    return decoded


if __name__ == '__main__':
    # Open and read YAML file:
    file = open("input.yml")
    file_content = yaml.safe_load(file)
    file.close()

    # Decoding token file:
    token_file = open("encoded_token.txt")
    token = token_decode(token_file)
    token_file.close()

    # Initiating my custom object:
    mgmtZone = ManagementZones(file_content, token)

    # Iterate through all the teams defined in yaml file:
    for title in mgmtZone.Teams.keys():
        # Generating payload for each management zone title:
        payload = dict(name=title, rules=[])
        if "host-group-prefixes" in mgmtZone.Teams[title].keys():
            for prefix in mgmtZone.Teams[title]["host-group-prefixes"]:
                rule = mgmtZone.rule_gen(prefix)
                payload["rules"].append(rule)

        # Retrieving management zone, by name, if already exists:
        existent = mgmtZone.exists(title)

        # Initiate HTTP request accordingly:
        if bool(existent):
            if "values" in existent.keys():
                mgmtZone.post_mz(payload)
            else:
                mgmtZone.put_mz(payload, existent['id'])
