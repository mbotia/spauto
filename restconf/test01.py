import requests
import json
from requests.auth import HTTPBasicAuth

url = 'https://192.168.200.81/api/monitoring/device/components/version'
auth = HTTPBasicAuth('cisco', 'cisco')

response = requests.get( url,  verify=False, auth=auth)

if response.status_code == 200:
    print ('Status Code: ' + str(response.status_code))
    parse = json.loads(response.text)
    print (json.dumps(parse, indent=4))
else:
    print ('ERROR Code: ' + str(response.status_code))
'''
url = 'https://192.168.1.12/api/objects/networkobjects'
auth = HTTPBasicAuth('cisco', 'cisco')
payload = {
     "host": {
          "kind": "IPv4Address",
          "value": "10.10.10.118"
},
      "kind": "object#NetworkObj",
      "name": "web_server08",
      "objectId": "web_server08"
}
headers = { 'content-type': "application/json" }
response = requests.post( url, data=json.dumps(payload), headers=headers, verify=False, auth=auth)
if response.status_code == 201:
     print 'Status Code: ' + str(response.status_code)
      print response.headers
else:
     print 'ERROR Code: ' + str(response.status_code)
     print response.headers
'''