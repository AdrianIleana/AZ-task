from managementzones import ManagementZones

if __name__ == '__main__':
    file = open("input.yml")

    mgmtZone = ManagementZones(file)

    # Iterate through all the teams defined in yaml file:
    for title in mgmtZone.Teams.keys():
        # Generating payload for each management zone title:
        payload = dict()
        payload["name"] = title
        payload["rules"] = []
        if "host-group-prefixes" in mgmtZone.Teams[title].keys():
            for prefix in mgmtZone.Teams[title]["host-group-prefixes"]:
                rule = mgmtZone.rule_gen(prefix)
                payload["rules"].append(rule)

        # Checking if management zone already exists:
        existent = mgmtZone.exists(title)

        # Initiate request accordingly:
        if existent:
            mgmtZone.put_mz(payload, existent['id'])
        else:
            mgmtZone.post_mz(payload)
