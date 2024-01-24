import json
import sys
sys.path.append('PROJET-GNS/src/')
sys.path.append('src/')
from classes import class_reseau as classr
from classes import class_output as output
from functions import fct_reseau as fctr
from functions import fct_protocol_reg as fctp
from functions import fct_show as sh

reg = output.registrar()

file_path = 'network_intent_data.json'

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
link_dict = {}
i = 0       # router_id

for as_system in network_intent['AS']:
    # print(as_system['number'],as_system['protocol'])
    # create as_objects dans an dictionary as_dict
    as_name = f"as{as_system['number']}"
    as_instance = classr.autonomous_system(as_system['number'], as_system['protocol'], as_system["community"], as_system["community_number"])
    as_dict[as_name] = as_instance
    # loopback range
    loopback_dic[as_name] = as_system['loopback_range']



    for router in as_system['routers']:
        i += 1 
        # create router_objects dans an dictionary router_dic
        router_name = router['name']
        router_instance = classr.router(router_name)
        router_dic[router_name] = router_instance
        router_dic[router_name].router_id = f"{i}.{i}.{i}.{i}"
        # create register
        reg.create_register(router_dic[router_name].name)
        # add router to as
        fctr.add_router_to_as(router_dic[router_name], as_dict[as_name])
        
        interfaces = router['interfaces']
        # interface id
        j = 0
        link_list = []
        for interface in interfaces:
            # create interface_objects dans an dictionary router_interface_dic
            interface_name = f"{router_name}GigabitEthernet{j}"
            router_interface_instance = classr.interface(interface['name'])
            router_interface_dic[interface_name] = router_interface_instance
            # init interface
            fctr.init_interface(router_dic[router_name], router_interface_dic[interface_name])
            reg.add_entry(router_dic[router_name].name, router_interface_dic[interface_name].name)

            if interface['neighbor'] != '0':
                link = []
                link.append(router_name)
                link.append(interface['neighbor'])
                link.append(interface_name)
                link.append(f"{interface['neighbor']}GigabitEthernet{j}") 
                link_list.append(link)

            j += 1
        link_dict[router_name] = link_list


# distribute loopback ip for each router
for AS_name, AS in as_dict.items():
    print(loopback_dic[AS_name])
    fctr.as_auto_loopback(AS, loopback_dic[AS_name])
    # print(AS.as_id)
    for router in AS.routers.values():
        # print(router.router_id)
        fctr.as_loopback_plan(AS)
        # print(router.loopback)

for router, link_list in link_dict.items():
    for link in link_list:
        # print(router_dic[link[0]].all_interfaces[router_interface_dic[link[2]].name])
        if router_dic[link[0]].all_interfaces[router_interface_dic[link[2]].name] == 0:
            # print(link)
            fctr.local_link(router_dic[link[0]], router_dic[link[1]], router_interface_dic[link[2]], router_interface_dic[link[3]])

for AS in as_dict.values():
    AS.construct_link_dict()

for AS in as_dict.values():
    fctr.as_auto_addressing_for_link(AS, "2001:300::", as_dict)    
    # sh.show_as_router_address(AS)

neighbor_info = fctp.generate_eBGP_neighbor_info(as_dict)
# print("@neighbor_info: ",neighbor_info)

fctp.as_config_interfaces(as_dict,reg)
fctp.as_config_unused_interface_and_loopback0(as_dict,reg) 

for AS in as_dict.values():
    m = 0
    if AS.igp == "OSPF":
        fctp.as_enable_ospf(AS,reg)
        m += 1
    elif AS.igp == "RIP":
        fctp.as_enable_rip(AS,reg)
        m += 1
    if m == 1:
        fctp.as_enable_BGP(as_dict,neighbor_info,reg)

# reg.display(reg.general_register)



# sh.show_as_router_status(as_dict["as1"])
sh.show_as_loopback_plan(as_dict["as1"])
sh.show_as_loopback_plan(as_dict["as2"])
sh.show_as_router_address(as_dict["as1"])
# sh.show_as_router_status(as_dict["as2"])
sh.show_as_router_address(as_dict["as2"])

# print_dict_contents(as_dict)
# print_dict_contents(router_dic)
# print_dict_contents(router_interface_dic)
# print_dict_contents(link_dict)
    



reg.save_as_txt()