import class_reseau as classr
import fct_reseau as fctr
import fct_protocol_reg as fctp
import fct_show as sh
import class_output as output

reg = output.registrar()

as1 = classr.autonomous_system(1,"OSPF")
as2 = classr.autonomous_system(2,"RIP")
as_dict = {as1.as_id:as1,as2.as_id:as2} # as a global container of all objects

#3 router in AS1                                                                                    
r1 = classr.router()
r1.router_id = "1.1.1.1"
r2 = classr.router("ABR")
r2.router_id = "2.2.2.2"
r3 = classr.router("ABR")
r3.router_id = "3.3.3.3"
#3 router in AS2
r4 = classr.router("ABR")
r4.router_id = "4.4.4.4"
r5 = classr.router("ABR")
r5.router_id = "5.5.5.5"
r6 = classr.router("Internal")
r6.router_id = "6.6.6.6" 

for router in [r1,r2,r3,r4,r5,r6]:
    reg.create_register(router.router_id)
# reg.display(reg.general_register)

#init interfaces
r1eth0 = classr.interface("eth0")
r1eth1 = classr.interface("eth1")
r1eth2 = classr.interface("eth2")
for interface in [r1eth0,r1eth1,r1eth2]:
    fctr.init_interface(r1,interface)
    reg.add_entry(r1.router_id,interface.name)
r2eth0 = classr.interface("eth0")
r2eth1 = classr.interface("eth1")
r2eth2 = classr.interface("eth2")
for interface in [r2eth0,r2eth1,r2eth2]:
    fctr.init_interface(r2,interface)
    reg.add_entry(r2.router_id,interface.name)
r3eth0 = classr.interface("eth0")
r3eth1 = classr.interface("eth1")
r3eth2 = classr.interface("eth2")
for interface in [r3eth0,r3eth1,r3eth2]:
    fctr.init_interface(r3,interface)
    reg.add_entry(r3.router_id,interface.name)
r4eth0 = classr.interface("eth0")
r4eth1 = classr.interface("eth1")
r4eth2 = classr.interface("eth2")
for interface in [r4eth0,r4eth1,r4eth2]:
    fctr.init_interface(r4,interface)
    reg.add_entry(r4.router_id,interface.name)
r5eth0 = classr.interface("eth0")
r5eth1 = classr.interface("eth1")
r5eth2 = classr.interface("eth2")
for interface in [r5eth0,r5eth1,r5eth2]:
    fctr.init_interface(r5,interface)
    reg.add_entry(r5.router_id,interface.name)
r6eth0 = classr.interface("eth0")
r6eth1 = classr.interface("eth1")
r6eth2 = classr.interface("eth2")
for interface in [r6eth0,r6eth1,r6eth2]:
    fctr.init_interface(r6,interface)
    reg.add_entry(r6.router_id,interface.name)
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

fctr.local_link(r1,r2,r1eth0,r2eth0)
# print("r1 all_interfaces: ",r1.all_interfaces)
# print("r1 interface eth0 connected to: ",r1.interfaces['eth0'].connected_router)
fctr.local_link(r1,r3,r1eth1,r3eth1)
fctr.local_link(r2,r4,r2eth1,r4eth1)
# print("r2 all_interfaces: ",r2.all_interfaces)
# print("r2 interface eth1 connected to: ",r2.interfaces['eth1'].connected_router)
fctr.local_link(r3,r5,r3eth0,r5eth0)
fctr.local_link(r4,r6,r4eth0,r6eth0)
fctr.local_link(r5,r6,r5eth1,r6eth1)

as1.construct_link_dict()
as2.construct_link_dict()
# print("AS1 link_dict: ",as1.link_dict)
# print("AS2 link_dict: ",as2.link_dict)


fctr.as_auto_addressing_for_link(as1,"2001:300::",as_dict)#ok


# sh.show_as_router_address(as1)

fctr.as_auto_addressing_for_link(as2,"2001:300::",as_dict)#ok

    

neighbor_info = fctp.generate_eBGP_neighbor_info(as_dict) #ok
# print("@neighbor_info: ",neighbor_info)


fctp.as_enable_rip(as1,reg) #ok
fctp.as_enable_ospf(as2,reg) #ok
# reg.display(reg.general_register)

# sh.show_as_router_status(as1)




# print(fctp.find_eBGP_neighbor_info('4.4.4.4','eth1',neighbor_info)) #ok

fctp.as_enable_BGP(as_dict,as1.loopback_plan,neighbor_info,reg) #ok
reg.display(reg.general_register)

reg.save_as_txt()