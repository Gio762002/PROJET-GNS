import json
import class_reseau as classr
import fct_reseau as fctr
import fct_protocol as fctp

file_path = 'network_intent.json'

with open(file_path, 'r') as file:
    network_intent = json.load(file)

# print(network_intent)
# print() 

# # Traverse through AS (Autonomous Systems) and their routers
# for as_system in network_intent['AS']:
#     print(f"AS Number: {as_system['number']}")
#     for router in as_system['routers']:
#         print(f"  Router Name: {router['name']}")
#         print(f"  Router Type: {router['type']}")
#         interfaces = router['interfaces']
#         for interface in interfaces:
#             print(f"    Interface: {interface['name']}")
#             # Check if neighbor is present (not '0')
#             if interface['neighbor'] != '0':
#                 print(f"    Neighbor: {interface['neighbor']}")
#                 print(f"    Neighbor Interface: {interface['neighbor_interface']}")
#             else:
#                 print("    No Neighbor")
#         print()  # Blank line for separating different routers



as_dict = {}
router_dic = {}
router_interface_dic = {}
i = 0
for as_system in network_intent['AS']:
    print(as_system['number'],as_system['protocol'])
    # create as_objects dans an dictionary as_dict
    as_name = f"as{as_system['number']}"
    as_instance = classr.autonomous_system(as_system['number'],as_system['protocol'])
    as_dict[as_name] = as_instance
    # distribute loopback
    fctr.as_auto_loopback(as_dict[as_name], router['loopback_range'])

    for router in as_system['routers']:
        i += 1 
        router_instance = classr.router()
        print(router['name'])
        print(f"{i}.{i}.{i}.{i}")
        router_name = router['name']
        router_dic[router_name] = router_instance
        router_dic[router_name].router_id = f"{i}.{i}.{i}.{i}"

        fctr.add_router_to_as(router_dic[router_name], as_dict[as_name])
        
        interfaces = router['interfaces']
        for interface in interfaces:
            j = 0
            print(interface['name'])
            print(f"{router_name}eth{j}")
            interface_name = f"{router_name}eth{j}"
            router_interface_instance = classr.interface(interface['name'])
            router_interface_dic[interface_name] = router_interface_instance
            fctr.init_interface(router_name, router_interface_dic[interface_name])

              
