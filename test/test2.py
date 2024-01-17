import json
import sys
import class_reseau as classr
import class_output as output
import fct_reseau as fctr
import fct_protocol_reg as fctp
import fct_show as sh

reg = output.registrar()

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
loopback_dic = {}
i = 0       # router_id

for as_system in network_intent['AS']:
    # print(as_system['number'],as_system['protocol'])
    # create as_objects dans an dictionary as_dict
    as_name = f"as{as_system['number']}"
    as_instance = classr.autonomous_system(as_system['number'],as_system['protocol'])
    as_dict[as_name] = as_instance

    loopback_dic[as_name] = as_system['loopback_range']

    for router in as_system['routers']:
        i += 1 
        # create router_objects dans an dictionary router_dic
        router_instance = classr.router()
        router_name = router['name']
        router_dic[router_name] = router_instance
        router_dic[router_name].router_id = f"{i}.{i}.{i}.{i}"
        # create register
        reg.create_register(router_dic[router_name].router_id)
        # add router to as
        fctr.add_router_to_as(router_dic[router_name], as_dict[as_name])
        
        interfaces = router['interfaces']
        # interface id
        j = 0
        for interface in interfaces:
            # create interface_objects dans an dictionary router_interface_dic
            interface_name = f"{router_name}eth{j}"
            router_interface_instance = classr.interface(interface['name'])
            router_interface_dic[interface_name] = router_interface_instance
            # init interface
            fctr.init_interface(router_dic[router_name], router_interface_dic[interface_name])
            reg.add_entry(router_dic[router_name].router_id, router_interface_dic[interface_name].name)

            j += 1

# distribute loopback ip for each router
for AS_name, AS in as_dict.items():
    print(loopback_dic[AS_name])
    fctr.as_auto_loopback(AS, loopback_dic[AS_name])
    print(AS.as_id)
    for router in AS.routers.values():
        print(router.router_id)
        fctr.as_loopback_plan(AS)
        print(router.loopback)




# def print_dict_contents(input_dict):
#     for key, value in input_dict.items():
#         print(f"Key: {key}, Value: {value}")
#     print()

# print_dict_contents(as_dict)
# print_dict_contents(router_dic)
# print_dict_contents(router_interface_dic)
