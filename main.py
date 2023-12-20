import class_reseau as classr
import fct_reseau as fctr


as1 = classr.autonomous_system(1,"OSPF")
as2 = classr.autonomous_system(2,"RIP")
    
print("AS1 id: ",as1.as_id)
print("AS1 igp: ",as1.igp)
print("AS2 id: ",as2.as_id)
print("AS2 igp: ",as2.igp)

r1 = classr.router("ABR")
r1.router_id = "1.1.1.1"
r2 = classr.router("Internal")
r2.router_id = "2.2.2.2"
print("r1 type: ",r1.type)
print("r2 type: ",r2.type)    


r1eth0 = classr.interface("eth0")
r1eth1 = classr.interface("eth1")
fctr.init_interface(r1,r1eth0)
fctr.init_interface(r1,r1eth1)
print("r1 all_interfaces: ",r1.all_interfaces)
print("r1 interfaces: ",r1.interfaces)

r2eth0 = classr.interface("eth0")
fctr.init_interface(r2,r2eth0)

fctr.set_interface(r1,r1eth0,r2,r2eth0)
print("r1 all_interfaces: ",r1.all_interfaces)

fctr.add_router_to_as(r1,as1)
print("AS1 routers: ",as1.routers)

fctr.delete_link(r1,r2)
print("r1 all_interfaces: ",r1.all_interfaces)
print("r1 interfaces: ",r1.interfaces)



#list_as = [as1,as2] ##need a general list of AS