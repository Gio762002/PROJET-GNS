import json
import os

network_intent_data = {
  "AS": [
    {
      "number": "1",
      "IP_range":"2001.127.100.0::/64",
      "loopback_range":"2001:100::",
      "protocol":"OSPF",
      "community": "customer",
      "community_number": "101",
      "routers": [
        {
          "name": "R1",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": [
            {
              "name": "GigabitEthernet0/0",
              "neighbor": "0",
              "neighbor_interface": "0"      
            },
            {
              "name": "GigabitEthernet1/0",
              "neighbor": "R2",
              "neighbor_interface": "GigabitEthernet1/0"      
            },
            {
              "name": "GigabitEthernet2/0",
              "neighbor": "R3",
              "neighbor_interface": "GigabitEthernet2/0"      
            },
            {
              "name": "GigabitEthernet3/0",
              "neighbor": "0",
              "neighbor_interface": "0"      
            },                      
          ],
        },
        
        {
          "name": "R2",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": [
            {
              "name": "GigabitEthernet0/0",
              "neighbor": "R4",
              "neighbor_interface": "GigabitEthernet0/0"      
            },
            {
              "name": "GigabitEthernet1/0",
              "neighbor": "R1",
              "neighbor_interface": "GigabitEthernet1/0"      
            },
            {
              "name": "GigabitEthernet2/0",
              "neighbor": "0",
              "neighbor_interface": "0"      
            },
            {
              "name": "GigabitEthernet3/0",
              "neighbor": "R3",
              "neighbor_interface": "GigabitEthernet3/0"      
            },                      
          ],
        },

        {
          "name": "R3",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": [
            {
              "name": "GigabitEthernet0/0",
              "neighbor": "R5",
              "neighbor_interface": "GigabitEthernet0/0"      
            },
            {
              "name": "GigabitEthernet1/0",
              "neighbor": "0",
              "neighbor_interface": "0"      
            },
            {
              "name": "GigabitEthernet2/0",
              "neighbor": "R1",
              "neighbor_interface": "GigabitEthernet2/0"      
            },
            {
              "name": "GigabitEthernet3/0",
              "neighbor": "R2",
              "neighbor_interface": "GigabitEthernet3/0"      
            },                      
          ],
        },

        {
          "name": "R4",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": [
            {
              "name": "GigabitEthernet0/0",
              "neighbor": "R2",
              "neighbor_interface": "GigabitEthernet0/0"      
            },
            {
              "name": "GigabitEthernet1/0",
              "neighbor": "R6",
              "neighbor_interface": "GigabitEthernet1/0"      
            },
            {
              "name": "GigabitEthernet2/0",
              "neighbor": "R7",
              "neighbor_interface": "GigabitEthernet2/0"      
            },
            {
              "name": "GigabitEthernet3/0",
              "neighbor": "R5",
              "neighbor_interface": "GigabitEthernet3/0"      
            },                      
          ],
        },

        {
          "name": "R5",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": [
            {
              "name": "GigabitEthernet0/0",
              "neighbor": "R3",
              "neighbor_interface": "GigabitEthernet0/0"      
            },
            {
              "name": "GigabitEthernet1/0",
              "neighbor": "R7",
              "neighbor_interface": "GigabitEthernet1/0"      
            },
            {
              "name": "GigabitEthernet2/0",
              "neighbor": "R6",
              "neighbor_interface": "GigabitEthernet2/0"      
            },
            {
              "name": "GigabitEthernet3/0",
              "neighbor": "R4",
              "neighbor_interface": "GigabitEthernet3/0"      
            },                      
          ],
        },

        {
          "name": "R6",
          "type": "eBGP",
          "bgp_preference": 100,
          "interfaces": [
            {
              "name": "GigabitEthernet0/0",
              "neighbor": "R8",
              "neighbor_interface": "GigabitEthernet0/0"      
            },
            {
              "name": "GigabitEthernet1/0",
              "neighbor": "R4",
              "neighbor_interface": "GigabitEthernet1/0"      
            },
            {
              "name": "GigabitEthernet2/0",
              "neighbor": "R5",
              "neighbor_interface": "GigabitEthernet2/0"      
            },
            {
              "name": "GigabitEthernet3/0",
              "neighbor": "0",
              "neighbor_interface": "0"      
            },                      
          ],
        },

        {
          "name": "R7",
          "type": "eBGP",
          "bgp_preference": 100,
          "interfaces": [
            {
              "name": "GigabitEthernet0/0",
              "neighbor": "R9",
              "neighbor_interface": "GigabitEthernet0/0"      
            },
            {
              "name": "GigabitEthernet1/0",
              "neighbor": "R5",
              "neighbor_interface": "GigabitEthernet1/0"      
            },
            {
              "name": "GigabitEthernet2/0",
              "neighbor": "R4",
              "neighbor_interface": "GigabitEthernet2/0"      
            },
            {
              "name": "GigabitEthernet3/0",
              "neighbor": "0",
              "neighbor_interface": "0"      
            },                      
          ],
        },
      ]
    },

    {
      "number": "2",
      "IP_range":"2001.127.200.0::/64",
      "loopback_range":"2001:200::",
      "protocol":"RIP",
      "community": "provider",
      "community_number": "102",
      "routers": [
        {
          "name": "R8",
          "type": "eBGP",
          "bgp_preference": 100,
          "interfaces": [
            {
              "name": "GigabitEthernet0/0",
              "neighbor": "R6",
              "neighbor_interface": "GigabitEthernet0/0"      
            },
            {
              "name": "GigabitEthernet1/0",
              "neighbor": "R10",
              "neighbor_interface": "GigabitEthernet1/0"      
            },
            {
              "name": "GigabitEthernet2/0",
              "neighbor": "R11",
              "neighbor_interface": "GigabitEthernet2/0"      
            },
            {
              "name": "GigabitEthernet3/0",
              "neighbor": "0",
              "neighbor_interface": "0"      
            },                      
          ],
        },

        {
          "name": "R9",
          "type": "eBGP",
          "bgp_preference": 100,
          "interfaces": [
            {
              "name": "GigabitEthernet0/0",
              "neighbor": "R7",
              "neighbor_interface": "GigabitEthernet0/0"      
            },
            {
              "name": "GigabitEthernet1/0",
              "neighbor": "R11",
              "neighbor_interface": "GigabitEthernet1/0"      
            },
            {
              "name": "GigabitEthernet2/0",
              "neighbor": "R10",
              "neighbor_interface": "GigabitEthernet2/0"      
            },
            {
              "name": "GigabitEthernet3/0",
              "neighbor": "0",
              "neighbor_interface": "0"      
            },                      
          ],
        },

        {
          "name": "R10",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": [
            {
              "name": "GigabitEthernet0/0",
              "neighbor": "R12",
              "neighbor_interface": "GigabitEthernet0/0"      
            },
            {
              "name": "GigabitEthernet1/0",
              "neighbor": "R8",
              "neighbor_interface": "GigabitEthernet1/0"      
            },
            {
              "name": "GigabitEthernet2/0",
              "neighbor": "R9",
              "neighbor_interface": "GigabitEthernet2/0"      
            },
            {
              "name": "GigabitEthernet3/0",
              "neighbor": "R11",
              "neighbor_interface": "GigabitEthernet3/0"      
            },                      
          ],
        },

        {
          "name": "R11",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": [
            {
              "name": "GigabitEthernet0/0",
              "neighbor": "R13",
              "neighbor_interface": "GigabitEthernet0/0"      
            },
            {
              "name": "GigabitEthernet1/0",
              "neighbor": "R9",
              "neighbor_interface": "GigabitEthernet1/0"      
            },
            {
              "name": "GigabitEthernet2/0",
              "neighbor": "R8",
              "neighbor_interface": "GigabitEthernet2/0"      
            },
            {
              "name": "GigabitEthernet3/0",
              "neighbor": "R10",
              "neighbor_interface": "GigabitEthernet3/0"      
            },                      
          ],
        },

        {
          "name": "R12",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": [
            {
              "name": "GigabitEthernet0/0",
              "neighbor": "R10",
              "neighbor_interface": "GigabitEthernet0/0"      
            },
            {
              "name": "GigabitEthernet1/0",
              "neighbor": "R14",
              "neighbor_interface": "GigabitEthernet1/0"      
            },
            {
              "name": "GigabitEthernet2/0",
              "neighbor": "0",
              "neighbor_interface": "0"      
            },
            {
              "name": "GigabitEthernet3/0",
              "neighbor": "R13",
              "neighbor_interface": "GigabitEthernet3/0"      
            },                      
          ],
        },

        {
          "name": "R13",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": [
            {
              "name": "GigabitEthernet0/0",
              "neighbor": "R11",
              "neighbor_interface": "GigabitEthernet0/0"      
            },
            {
              "name": "GigabitEthernet1/0",
              "neighbor": "0",
              "neighbor_interface": "0"      
            },
            {
              "name": "GigabitEthernet2/0",
              "neighbor": "R14",
              "neighbor_interface": "GigabitEthernet2/0"      
            },
            {
              "name": "GigabitEthernet3/0",
              "neighbor": "R12",
              "neighbor_interface": "GigabitEthernet3/0"      
            },                      
          ],
        },

        {
          "name": "R14",
          "type": "iBGP",
          "bgp_preference": 100,
          "interfaces": [
            {
              "name": "GigabitEthernet0/0",
              "neighbor": "0",
              "neighbor_interface": "0"      
            },
            {
              "name": "GigabitEthernet1/0",
              "neighbor": "R12",
              "neighbor_interface": "GigabitEthernet1/0"      
            },
            {
              "name": "GigabitEthernet2/0",
              "neighbor": "R13",
              "neighbor_interface": "GigabitEthernet2/0"      
            },
            {
              "name": "GigabitEthernet3/0",
              "neighbor": "0",
              "neighbor_interface": "0"      
            },                      
          ],
        },
      ]
    }
  ]
}

file_path = '/network_intent_data.json'
if os.path.exists(file_path): 
    os.remove(file_path)
with open(file_path, 'w') as file:
    json.dump(network_intent_data, file, indent=4)

