import json
import sys
# sys.path.append('PROJET-GNS/src/')
sys.path.append('src/')
from classes import class_reseau as classr
from classes import class_output as output
from functions import fct_reseau as fctr
from functions import fct_protocol_reg as fctp
from functions import fct_show as sh

reg = output.registrar() #creation of an registrar instence

#load the intent file
file = "network_intent_data.json"
with open(file,"r") as f:
    network_intent = json.load(f)

'''
In Python, dynamically generating variable names is not a good programming practice so :( 
dictionarie as_dict is created to track As instances. 
For other router/interface instances, once they are created, they are binded to their As directly.
So they are not tracked by any other data structure as As is, thanks to classes we defined.
'''
as_dict = {}

"""read the intent file, 'simulate' its topologie"""
for json_as in network_intent['AS']: # json_as is a dict
    as_name = f"as{json_as['number']}"
    as_instance = classr.autonomous_system(json_as['number'], 
                                           json_as['loopback_range'],
                                           json_as['IP_range'],
                                           json_as['protocol'], 
                                           json_as['community'], 
                                           json_as['community_number'])
    as_dict[as_name] = as_instance

    for json_router in json_as['routers']: # json_router is a dict
        router_name = json_router['name']
        router_instance = classr.router(router_name, json_router['type'])
        router_instance.get_router_id()
        fctr.add_router_to_as(router_instance,as_instance) # bind to as
        
        reg.create_register(router_instance.name) # creat a register for the router

        for json_interface in json_router['interfaces']: # json_interface is a dict
            interface_name = f"{router_name}{json_interface['name']}" #something like 'R1GigabitEthernet1/0'
            interface_instance = classr.interface(json_interface['name'])
            fctr.init_interface(router_instance,interface_instance) # bind to router
            
            if json_interface['neighbor'] != '':
                neighbor_id = ((json_interface['neighbor'][1:]+".")*4)[:-1] #all functions use router_id as an index, and they were wrote first so sorry for neighbor.
                as_instance.link_dict[(router_instance.router_id, interface_instance.name)] = (neighbor_id, json_interface['neighbor_interface'])
            as_instance.eliminate_repeat_link()

            reg.add_entry(router_instance.name,interface_instance.name) #add entry to the register of its router
    
    as_instance.auto_loopback()
    as_instance.generate_loopback_plan()

fctr.as_local_links(as_dict)
fctr.as_auto_addressing_for_link(as_dict) # from now on, everything is placed so can be tracked by attributes, what is left is to implement the protocols.

fctp.as_config_interfaces(as_dict, reg)
fctp.as_config_unused_interface_and_loopback0(as_dict, reg)

"""implement the protocols"""
neighbor_info = fctp.generate_eBGP_neighbor_info(as_dict)
try:
    fctp.as_enable_BGP(as_dict, neighbor_info, reg)
except Exception as e:
    print("Error implementing BGP : ", e)

for As in as_dict.values():
    try:
        if As.igp == "OSPF":
            fctp.as_enable_ospf(As, reg)
        elif As.igp == "RIP":
            fctp.as_enable_rip(As, reg)
    except Exception as e:
        print("Error implementing IGP protocols : ", e)

"""implement routing policies"""
fctp.as_config_local_pref(as_dict, neighbor_info, reg)

"""output the configuration files"""
reg.save_as_cfg()
# reg.display(reg.general_register)
