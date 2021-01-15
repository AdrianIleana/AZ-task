from managementzones import ManagementZones

if __name__ == '__main__':
    file = open("input.yml")

    mgmtZone = ManagementZones(file)

    zones_from_dt = mgmtZone.get_mz()

    for title in mgmtZone.Teams.keys():
        payload = dict()
        payload["name"] = title
        payload["rules"] = []
        if "host-group-prefixes" in mgmtZone.Teams[title].keys():
            for prefix in mgmtZone.Teams[title]["host-group-prefixes"]:
                rule = mgmtZone.rule_gen(prefix)
                payload["rules"].append(rule)
        if mgmtZone.exists_in(title, zones_from_dt['values']):
            zone = mgmtZone.exists_in(title, zones_from_dt['values'])
            mgmtZone.put_mz(payload, zone['id'])
        else:
            mgmtZone.post_mz(payload)
