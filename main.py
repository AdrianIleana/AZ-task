from MzApi import MzApi


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


if __name__ == '__main__':
    file = open("input.yml")

    api = MzApi(file)

    mgmt_zones = api.get_mz()

    for title in api.Teams.keys():
        payload = dict()
        payload["name"] = title
        if "host-group-prefixes" in api.Teams[title].keys():
            list_of_rules = []
            for prefix in api.Teams[title]["host-group-prefixes"]:
                rule = rule_gen(prefix)
                list_of_rules.append(rule)
            payload["rules"] = list_of_rules
        if api.is_existing_mz(title, mgmt_zones['values']):
            zone = api.is_existing_mz(title, mgmt_zones['values'])
            api.put_mz(payload, zone['id'])
        else:
            api.post_mz(payload)
