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
In Python, dynamically generating variable names is not a good programming practice but... :( 
dictionaries are created to track instances
'''
as_dict = {}
router_dic = {}
interface_dic = {}
loopback_dic = {}
link_dict = {}

# read the intent file, 'simulate' its topologie
for json_as in network_intent['AS']: # json_as is a dict
    as_name = f"as{json_as['number']}"
    as_instance = classr.autonomous_system(json_as['number'], 
                                           json_as['loopback_range'],
                                           json_as['protocol'], 
                                           json_as['community'], 
                                           json_as['community_number'])
    as_dict[as_name] = as_instance # put inside the dict for further use


    for json_router in json_as['routers']: # json_router is a dict
        router_name = json_router['name']
        router_instance = classr.router(router_name)
        router_instance.get_router_id()
        fctr.add_router_to_as(router_instance,as_instance) # bind to as
        
        reg.create_register(router_instance.name) # creat a register for the router
        router_dic[router_name] = router_instance # put inside the dict for further use


        for json_interface in json_router['interfaces']: # json_interface is a dict
            interface_name = f"{router_name}{json_interface['name']}" #something like 'R1GigabitEthernet1/0'
            interface_instance = classr.interface(json_interface['name'])
            fctr.init_interface(router_instance,interface_instance) # bind to router
            
            if json_interface['neighbor'] != '':
                neighbor_id = ((json_interface['neighbor'][1:]+".")*4)[:-1]
                as_instance.link_dict[(router_instance.router_id, interface_instance.name)] = (neighbor_id, json_interface['neighbor_interface'])
            

            reg.add_entry(router_instance.name,interface_instance.name)
            interface_dic[interface_name] = interface_instance # put inside the dict for further use
    
    as_instance.auto_loopback()
    as_instance.generate_loopback_plan()

# for As in as_dict.values():
#     print("As",As.as_id,":",As.routers)
fctr.as_local_links(as_dict)
for As in as_dict.values():
    for router in As.routers.values():
        for interface in router.interfaces.values():
            print(router.name,"#",interface.name," is ",interface.statu," connet to ",interface.connected_router," via ",interface.connected_interface)
            print("protocol:",interface.igp_protocol_type," egp:",interface.egp_protocol_type,"running",interface.protocol_process)
