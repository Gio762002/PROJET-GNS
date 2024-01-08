import json

network_intent_data = {
  "AS": [
    {
      "number": "1",
      "IP_range":"2001.127.100.0::/64",
      "loopback_range":"100::/128",
      "protocol":"RIP",
      "routers": [
        {
          "name": "R1",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": ["GigabitEthernet0/0","GigabitEthernet0/1","GigabitEthernet0/2","GigabitEthernet0/3"],
          "neighbor": ["R2","R3"]
        },

        {
          "name": "R2",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": ["GigabitEthernet0/0","GigabitEthernet0/1","GigabitEthernet0/2","GigabitEthernet0/3"],
          "neighbor": ["R1","R3","R4"]
        },

        {
          "name": "R3",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": ["GigabitEthernet0/0","GigabitEthernet0/1","GigabitEthernet0/2","GigabitEthernet0/3"],
          "neighbor": ["R1","R2","R5"]
        },

        {
          "name": "R4",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": ["GigabitEthernet0/0","GigabitEthernet0/1","GigabitEthernet0/2","GigabitEthernet0/3"],
          "neighbor": ["R2","R5","R6","R7"]
        },

        {
          "name": "R5",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": ["GigabitEthernet0/0","GigabitEthernet0/1","GigabitEthernet0/2","GigabitEthernet0/3"],
          "neighbor": ["R3","R4","R6","R7"]
        },

        {
          "name": "R6",
          "type": "eBGP",
          "bgp_preference": 100,
          "interfaces": ["GigabitEthernet0/0","GigabitEthernet0/1","GigabitEthernet0/2","GigabitEthernet0/3"],
          "neighbor": ["R4","R5","R8"]
        },

        {
          "name": "R7",
          "type": "eBGP",
          "bgp_preference": 100,
          "interfaces": ["GigabitEthernet0/0","GigabitEthernet0/1","GigabitEthernet0/2","GigabitEthernet0/3"],
          "neighbor": ["R4","R5","R9"]
        },
      ]
    },

    {
      "number": "2",
      "IP_range":"2001.127.200.0::/64",
      "loopback_range":"200::/128",
      "protocol":"OSPF",
      "routers": [
        {
          "name": "R8",
          "type": "eBGP",
          "bgp_preference": 100,
          "interfaces": ["GigabitEthernet0/0","GigabitEthernet0/1","GigabitEthernet0/2","GigabitEthernet0/3"],
          "neighbor": ["R6","R10","R11"]
        },

        {
          "name": "R9",
          "type": "eBGP",
          "bgp_preference": 100,
          "interfaces": ["GigabitEthernet0/0","GigabitEthernet0/1","GigabitEthernet0/2","GigabitEthernet0/3"],
          "neighbor": ["R7","R10","R11"]
        },

        {
          "name": "R10",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": ["GigabitEthernet0/0","GigabitEthernet0/1","GigabitEthernet0/2","GigabitEthernet0/3"],
          "neighbor": ["R8","R9","R11","R12"]
        },

        {
          "name": "R11",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": ["GigabitEthernet0/0","GigabitEthernet0/1","GigabitEthernet0/2","GigabitEthernet0/3"],
          "neighbor": ["R8","R9","R10","R13"]
        },

        {
          "name": "R12",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": ["GigabitEthernet0/0","GigabitEthernet0/1","GigabitEthernet0/2","GigabitEthernet0/3"],
          "neighbor": ["R10","R13","R14"]
        },

        {
          "name": "R13",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": ["GigabitEthernet0/0","GigabitEthernet0/1","GigabitEthernet0/2","GigabitEthernet0/3"],
          "neighbor": ["R11","R12","R14"]
        },

        {
          "name": "R14",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": ["GigabitEthernet0/0","GigabitEthernet0/1","GigabitEthernet0/2","GigabitEthernet0/3"],
          "neighbor": ["R12","R13"]
        },
      ]
    }
  ]
}

file_path = 'network_intent.json'

with open(file_path, 'w') as file:
    json.dump(network_intent_data, file, indent=4)