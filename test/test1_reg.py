import sys
sys.path.append('PROJET-GNS/src/')
sys.path.append('src/')
from classes import class_reseau as classr
from classes import class_output as output
from functions import fct_reseau as fctr
from functions import fct_protocol_reg as fctp
from functions import fct_show as sh


reg = output.registrar()

as1 = classr.autonomous_system(1,"OSPF","customer",101)
as2 = classr.autonomous_system(2,"RIP","provider",102)
as_dict = {as1.as_id:as1,as2.as_id:as2} # as a global container of all objects

#3 router in AS1                                                                                    
r1 = classr.router("r1")
r1.router_id = "1.1.1.1"
r2 = classr.router("r2","ABR")
r2.router_id = "2.2.2.2"
r3 = classr.router("r3","ABR")
r3.router_id = "3.3.3.3"
#3 router in AS2
r4 = classr.router("r4","ABR")
r4.router_id = "4.4.4.4"
r5 = classr.router("r5","ABR")
r5.router_id = "5.5.5.5"
r6 = classr.router("r6","Internal")
r6.router_id = "6.6.6.6" 

for router in [r1,r2,r3,r4,r5,r6]:
    reg.create_register(router.name)
# reg.display(reg.general_register)

#init interfaces
r1GigabitEthernet0 = classr.interface("GigabitEthernet0/0")
r1GigabitEthernet1 = classr.interface("GigabitEthernet1/0")
r1GigabitEthernet2 = classr.interface("GigabitEthernet2/0")
for interface in [r1GigabitEthernet0,r1GigabitEthernet1,r1GigabitEthernet2]:
    fctr.init_interface(r1,interface)
    reg.add_entry(r1.name,interface.name)
r2GigabitEthernet0 = classr.interface("GigabitEthernet0/0")
r2GigabitEthernet1 = classr.interface("GigabitEthernet1/0")
r2GigabitEthernet2 = classr.interface("GigabitEthernet2/0")
for interface in [r2GigabitEthernet0,r2GigabitEthernet1,r2GigabitEthernet2]:
    fctr.init_interface(r2,interface)
    reg.add_entry(r2.name,interface.name)
r3GigabitEthernet0 = classr.interface("GigabitEthernet0/0")
r3GigabitEthernet1 = classr.interface("GigabitEthernet1/0")
r3GigabitEthernet2 = classr.interface("GigabitEthernet2/0")
for interface in [r3GigabitEthernet0,r3GigabitEthernet1,r3GigabitEthernet2]:
    fctr.init_interface(r3,interface)
    reg.add_entry(r3.name,interface.name)
r4GigabitEthernet0 = classr.interface("GigabitEthernet0/0")
r4GigabitEthernet1 = classr.interface("GigabitEthernet1/0")
r4GigabitEthernet2 = classr.interface("GigabitEthernet2/0")
for interface in [r4GigabitEthernet0,r4GigabitEthernet1,r4GigabitEthernet2]:
    fctr.init_interface(r4,interface)
    reg.add_entry(r4.name,interface.name)
r5GigabitEthernet0 = classr.interface("GigabitEthernet0/0")
r5GigabitEthernet1 = classr.interface("GigabitEthernet1/0")
r5GigabitEthernet2 = classr.interface("GigabitEthernet2/0")
for interface in [r5GigabitEthernet0,r5GigabitEthernet1,r5GigabitEthernet2]:
    fctr.init_interface(r5,interface)
    reg.add_entry(r5.name,interface.name)
r6GigabitEthernet0 = classr.interface("GigabitEthernet0/0")
r6GigabitEthernet1 = classr.interface("GigabitEthernet1/0")
r6GigabitEthernet2 = classr.interface("GigabitEthernet2/0")
for interface in [r6GigabitEthernet0,r6GigabitEthernet1,r6GigabitEthernet2]:
    fctr.init_interface(r6,interface)
    reg.add_entry(r6.name,interface.name)
# reg.display(reg.general_register)

for router in [r1,r2,r3]:
    fctr.add_router_to_as(router,as1)
for router in [r4,r5,r6]:
    fctr.add_router_to_as(router,as2)

fctr.as_auto_loopback(as1,"2001:100::")
fctr.as_auto_loopback(as2,"2001:200::")
for router in as1.routers.values():
    fctr.as_loopback_plan(as1)
for router in as2.routers.values():
    fctr.as_loopback_plan(as2)
# sh.show_as_loopback_plan(as1)

fctr.local_link(r1,r2,r1GigabitEthernet0,r2GigabitEthernet0)
# print("r1 all_interfaces: ",r1.all_interfaces)
# print("r1 interface GigabitEthernet0 connected to: ",r1.interfaces['GigabitEthernet0'].connected_router)
fctr.local_link(r1,r3,r1GigabitEthernet1,r3GigabitEthernet1)
fctr.local_link(r2,r4,r2GigabitEthernet1,r4GigabitEthernet1)
# print("r2 all_interfaces: ",r2.all_interfaces)
# print("r2 interface GigabitEthernet1 connected to: ",r2.interfaces['GigabitEthernet1'].connected_router)
fctr.local_link(r3,r5,r3GigabitEthernet0,r5GigabitEthernet0)
fctr.local_link(r4,r6,r4GigabitEthernet0,r6GigabitEthernet0)
fctr.local_link(r5,r6,r5GigabitEthernet1,r6GigabitEthernet1)

as1.construct_link_dict()
as2.construct_link_dict()
# print("AS1 link_dict: ",as1.link_dict)
# print("AS2 link_dict: ",as2.link_dict)


fctr.as_auto_addressing_for_link(as1,"2001:300::",as_dict)#ok


# sh.show_as_router_address(as1)

fctr.as_auto_addressing_for_link(as2,"2001:300::",as_dict)#ok

    

neighbor_info = fctp.generate_eBGP_neighbor_info(as_dict) #ok 

fctp.as_config_interfaces(as_dict,reg)
fctp.as_config_unused_interface_and_loopback0(as_dict,reg) 

fctp.set_community("r2", "SET_COMMUNITY", "101", reg)
fctp.filter_community("r3", "FILTER_COMMUNITY", "101", reg)
fctp.tag_community("r4", "LISTNAME", "TAG_COMMUNITY", "102","provider", reg)

fctp.as_enable_rip(as1,reg) #ok
fctp.as_enable_BGP(as_dict,neighbor_info,reg,True) 
fctp.as_enable_ospf(as2,reg) #ok


# reg.display(reg.general_register)

# sh.show_as_router_status(as1)
sh.show_as_loopback_plan(as1)
sh.show_as_loopback_plan(as2)
sh.show_as_router_address(as1)
# sh.show_as_router_status(as2)
sh.show_as_router_address(as2)

# print(fctp.find_eBGP_neighbor_info('4.4.4.4','GigabitEthernet1',neighbor_info)) #ok

#ok
# reg.display(reg.general_register)

reg.save_as_txt()

