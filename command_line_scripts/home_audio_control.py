import requests, json, credentials
from sys import argv

# parse the command line
# -c comand, -z zone, -v value
opts = {}
while argv:
    if argv[0][0] == '-':
        opts[argv[0]] = argv[1]
    argv = argv[1:] 


# switch the power
payload = { 'command': opts['-c'], 'zone': opts['-z'], 'value': opts['-v'] }
r=requests.get("http://192.168.1.17:8080/mca66", params=payload)
# print(r.url)

# parse the reply
zone_info=r.json()[str(opts['-z'])]

# adjust the slider in HA
if zone_info['power']=="on":
    vol_to_set = zone_info["vol"]
else:
    vol_to_set = 0

# set vol slider to match
data = {"entity_id": "input_number.slider"+opts['-z'],
        "value": str(vol_to_set) }
headers = { "x-ha-access": credentials.ha_pass,
            "content-type": "application/json"}
r=requests.post("https://hass.stevesell.com/api/services/input_number/set_value", 
                headers=headers, data=json.dumps(data))
# result=r.json()
# print(r.url)
# print(data)
