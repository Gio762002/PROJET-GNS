import json

file_path = 'network_intent.json'

with open(file_path, 'r') as file:
    network_intent = json.load(file)

print(network_intent)
print() 

# 遍历AS（Autonomous Systems）和它们的路由器
for as_system in network_intent['AS']:
    print(f"AS Number: {as_system['number']}")
    for router in as_system['routers']:
        print(f"  Router Name: {router['name']}")
        print(f"  Router Type: {router['type']}")
        print(f"  Interfaces: {', '.join(router['interfaces'])}")
        print(f"  Neighbors: {', '.join(router['neighbor'])}")
        print()  # 空行以分隔不同的路由器