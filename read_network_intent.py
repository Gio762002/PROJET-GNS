import json

file_path = 'network_intent.json'

with open(file_path, 'r') as file:
    network_intent = json.load(file)

print(network_intent)
print() 

# Traverse through AS (Autonomous Systems) and their routers
for as_system in network_intent['AS']:
    print(f"AS Number: {as_system['number']}")
    for router in as_system['routers']:
        print(f"  Router Name: {router['name']}")
        print(f"  Router Type: {router['type']}")
        interfaces = router['interfaces']
        for interface in interfaces:
            print(f"    Interface: {interface['name']}")
            # Check if neighbor is present (not '0')
            if interface['neighbor'] != '0':
                print(f"    Neighbor: {interface['neighbor']}")
                print(f"    Neighbor Interface: {interface['neighbor_interface']}")
            else:
                print("    No Neighbor")
        print()  # Blank line for separating different routers
