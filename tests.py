import unittest
from managementzones import ManagementZones
import requests


class TestManagementZones(unittest.TestCase):
    def test_PUT_mz(self):
        file = open("input.yml")
        test_payload = {
          "name": "Mainframe",
          "rules": [
            {
              "type": "SERVICE",
              "enabled": True,
              "propagationTypes": [
                "SERVICE_TO_PROCESS_GROUP_LIKE"
              ],
              "conditions": [
                {
                  "key": {
                    "attribute": "HOST_ARCHITECTURE"
                  },
                  "comparisonInfo": {
                    "type": "OS_ARCHITECTURE",
                    "operator": "EQUALS",
                    "value": "ARM",
                    "negate": False
                  }
                }
              ]
            }
          ]
        }

        mgmt_zone = ManagementZones(file)
        file.close()
        existent = mgmt_zone.exists(test_payload['name'])

        mgmt_zone.put_mz(test_payload, existent['id'])

        response = requests.get(
            mgmt_zone.URL + "/{}".format(existent['id']),
            headers=mgmt_zone.header
        )

        existent = response.json()

        for k in test_payload.keys():
            self.assertEqual(test_payload[k], existent[k])

    def test_POST_mz(self):
        file = open("input.yml")
        test_payload = {
          "name": "Mainframe",
          "rules": [
            {
              "type": "SERVICE",
              "enabled": True,
              "propagationTypes": [
                "SERVICE_TO_PROCESS_GROUP_LIKE"
              ],
              "conditions": [
                {
                  "key": {
                    "attribute": "HOST_ARCHITECTURE"
                  },
                  "comparisonInfo": {
                    "type": "OS_ARCHITECTURE",
                    "operator": "EQUALS",
                    "value": "ZOS",
                    "negate": False
                  }
                }
              ]
            }
          ]
        }

        mgmt_zone = ManagementZones(file)
        file.close()
        zones = mgmt_zone.get_mz()
        before = len(zones['values'])

        mgmt_zone.post_mz(test_payload)
        zones = mgmt_zone.get_mz()

        self.assertEqual(before + 1, len(zones['values']), "Unexpected number of management zones")


if __name__ == '__main__':
    unittest.main()
