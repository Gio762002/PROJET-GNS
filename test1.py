import class_reseau as classr
import fct_reseau as fctr
import fct_protocol as fctp

as1 = classr.autonomous_system(1,"OSPF")
as2 = classr.autonomous_system(2,"RIP")
as_lst = [as1,as2] # as a global container of all objects

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


#init interfaces
r1eth0 = classr.interface("eth0")
r1eth1 = classr.interface("eth1")
r1eth2 = classr.interface("eth2")
for interface in [r1eth0,r1eth1,r1eth2]:
    fctr.init_interface(r1,interface)
r2eth0 = classr.interface("eth0")
r2eth1 = classr.interface("eth1")
r2eth2 = classr.interface("eth2")
for interface in [r2eth0,r2eth1,r2eth2]:
    fctr.init_interface(r2,interface)
r3eth0 = classr.interface("eth0")
r3eth1 = classr.interface("eth1")
r3eth2 = classr.interface("eth2")
for interface in [r3eth0,r3eth1,r3eth2]:
    fctr.init_interface(r3,interface)
r4eth0 = classr.interface("eth0")
r4eth1 = classr.interface("eth1")
r4eth2 = classr.interface("eth2")
for interface in [r4eth0,r4eth1,r4eth2]:
    fctr.init_interface(r4,interface)
r5eth0 = classr.interface("eth0")
r5eth1 = classr.interface("eth1")
r5eth2 = classr.interface("eth2")
for interface in [r5eth0,r5eth1,r5eth2]:
    fctr.init_interface(r5,interface)
r6eth0 = classr.interface("eth0")
r6eth1 = classr.interface("eth1")
r6eth2 = classr.interface("eth2")
for interface in [r6eth0,r6eth1,r6eth2]:
    fctr.init_interface(r6,interface)


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
# print("AS1 loopback plan: ",as2.loopback_plan) checked
# print(r1.interfaces[r1.loopback_interface].tag)

fctr.local_link(r1,r2)
# print("r1 all_interfaces: ",r1.all_interfaces)
# print("r1 interface eth1 connected to: ",r1.interfaces['eth1'].connected_router)
fctr.local_link(r1,r3)
fctr.local_link(r2,r4)
# print("r2 all_interfaces: ",r2.all_interfaces)
# print("r2 interface eth1 connected to: ",r2.interfaces['eth2'].connected_router)
fctr.local_link(r3,r5)
fctr.local_link(r4,r6)
fctr.local_link(r5,r6)

as1.construct_link_lst()
as2.construct_link_lst()
print("AS1 link_lst: ",as1.link_lst)
print("AS2 link_lst: ",as2.link_lst)

'''need to convert the code into a function'''
numero_link = 0
for ((rt1,int1),(rt2,int2)) in as1.link_lst: #all input are strings
    (address1,address2) = fctr.as_auto_addressing_for_link(as1,"2001:300::",int1,int2,numero_link)
    numero_link += 1
    if rt1 in as1.loopback_plan.keys():
        as1.routers[rt1].interfaces[int1].address_ipv6_global = address1
    elif rt1 in as2.loopback_plan.keys():
        as2.routers[rt1].interfaces[int1].address_ipv6_global = address1
    if rt2 in as1.loopback_plan.keys():
        as1.routers[rt2].interfaces[int2].address_ipv6_global = address2
    elif rt2 in as2.loopback_plan.keys():
        as2.routers[rt2].interfaces[int2].address_ipv6_global = address2

# for r in as1.routers.values():
    # for interface in r.interfaces.keys(): #interface as a string
        # print(r.router_id,":",interface,':',r.interfaces[interface].address_ipv6_global)
    # print(" ")
# print(r4.router_id,": eth1:",r4.interfaces['eth1'].address_ipv6_global)
# print(r5.router_id,": eth1:",r5.interfaces['eth1'].address_ipv6_global)
# print("")

numero_link = 0
for ((rt1,int1),(rt2,int2)) in as2.link_lst: #all input are strings
    (address1,address2) = fctr.as_auto_addressing_for_link(as2,"2001:300::",int1,int2,numero_link)
    numero_link += 1
    rtr = as1.routers.get(rt1) if rt1 in as1.routers.keys() else as2.routers.get(rt1)
    if rtr.interfaces.get(int1).address_ipv6_global is None:
        rtr.interfaces.get(int1).address_ipv6_global = address1
    rtr = as1.routers.get(rt2) if rt2 in as1.routers.keys() else as2.routers.get(rt2)
    if rtr.interfaces.get(int2).address_ipv6_global is None: #as1 dont have this check, should add
        rtr.interfaces.get(int2).address_ipv6_global = address2
# for rtr in as2.routers.values():
#     for interface in rtr.interfaces.keys(): #interface as a string
#         print(rtr.router_id,":",interface,':',rtr.interfaces[interface].address_ipv6_global)
#     print(" ")
   





# test for modifying config : delete link/ add link
fctr.delete_link(r1,r2,as_lst)
for interface in r1.interfaces.values():
    print(interface.name,":",interface.address_ipv6_global)
print(" ")
for interface in r2.interfaces.values():
    print(interface.name,":",interface.address_ipv6_global)
print(" ")

for As in as_lst:
    for rtr in As.routers.values():
        for interface in rtr.interfaces.values():
            print(rtr.router_id,":",interface.name,':',interface.address_ipv6_global)
        print(" ")
print("AS1 link_lst: ",as1.link_lst)
print("AS2 link_lst: ",as2.link_lst)