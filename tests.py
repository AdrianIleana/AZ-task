import unittest
from managementzones import ManagementZones
import yaml
import base64


class TestManagementZones(unittest.TestCase):
    def test_PUT_mz(self):
        file = open("input.yml")
        file_content = yaml.load(file, Loader=yaml.FullLoader)
        file.close()

        token_file = open("encoded_token.txt")
        base64_bytes = token_file.read().encode('ascii')
        text_to_bytes = base64.b64decode(base64_bytes)
        token = text_to_bytes.decode('ascii')
        token_file.close()

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

        mgmt_zone = ManagementZones(file_content, token)

        existent = mgmt_zone.exists(test_payload['name'])

        mz_id = existent['id']
        mgmt_zone.put_mz(test_payload, mz_id)

        existent = mgmt_zone.get_mz(mz_id)

        for k in test_payload.keys():
            self.assertEqual(test_payload[k], existent[k])

    def test_POST_mz(self):
        file = open("input.yml")
        file_content = yaml.load(file, Loader=yaml.FullLoader)
        file.close()

        token_file = open("encoded_token.txt")
        base64_bytes = token_file.read().encode('ascii')
        text_to_bytes = base64.b64decode(base64_bytes)
        token = text_to_bytes.decode('ascii')
        token_file.close()

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

        mgmt_zone = ManagementZones(file_content, token)

        zones = mgmt_zone.get_mz()
        before = len(zones['values'])

        mgmt_zone.post_mz(test_payload)
        zones = mgmt_zone.get_mz()

        self.assertEqual(before + 1, len(zones['values']), "Unexpected number of management zones")


if __name__ == '__main__':
    unittest.main()
