'''
Clarification : all full names (router/interface) refer to instances, and all abbrev refer to strings 
certains fcts have parameter : dict_as, which is a dict of all As instances that will be used in the main program
'''

def init_interface(router,interface):
    router.all_interfaces[interface.name] = 0 # .name is the key
    router.interfaces[interface.name] = interface

def reset_interface(router,int): # only one side
    router.all_interfaces[int] = 0
    router.interfaces[int].statu = "down"
    router.interfaces[int].connected_router = None
    router.interfaces[int].connected_interface = None
    router.interfaces[int].address_ipv6_global = None

'''need reset_interface'''
def delete_link(router1,router2,dict_as): # = reset_interface for both sides
    for interface in router1.interfaces.values():
        if interface.connected_router == router2.router_id:
            reset_interface(router1,interface.name)
    for interface in router2.interfaces.values():
        if interface.connected_router == router1.router_id:
            reset_interface(router2,interface.name)
    # uploade the As link list
    for As in dict_as.values():
        if As.as_id == router1.position or As.as_id == router2.position:
            As.update_link_dict(router1.router_id,router2.router_id)

def reinit_router(router,loopback,type): #router as an instance
    router.loopback = loopback
    router.type = type
 
def add_router_to_as(router,As): #router,As are instances
    As.routers[router.router_id] = router
    router.position = As.as_id #router.position is a string


'''three fcts concerning address distribution'''
#distribution of ipv6 addresses for an as
def get_router_instance(router_id,dict_as):
    for As in dict_as.values():
        if router_id in As.routers.keys():
            return As.routers.get(router_id)
    raise Exception("router_id not found")

def as_auto_addressing_for_link(dict_as): # ip_range = "2001:100::0", As as an instance, dict_as as a list of As instances
    for As in dict_as.values():    
        link_dict_copy = As.link_dict.copy()
        numero_link = 0
        for ((r1,i1),(r2,i2)) in As.link_dict.items(): #all are strings   
            if (r2,i2) in link_dict_copy.keys():
                del link_dict_copy[(r2,i2)]
            if (r1,i1) in link_dict_copy.keys():
                numero_link += 1
                s_address = As.ip_range[:-4] + str(As.as_id) + ":" + str(numero_link) + "::1"
                b_address = As.ip_range[:-4] + str(As.as_id) + ":" + str(numero_link) + "::2"
                if r1 > r2:
                    addresses = (b_address,s_address)          
                else:
                    addresses = (s_address,b_address)# router having bigger id has bigger address
            router1 = get_router_instance(r1,dict_as)
            router2 = get_router_instance(r2,dict_as)
            if router1.interfaces.get(i1).address_ipv6_global is None:
                router1.interfaces.get(i1).address_ipv6_global = addresses[0]
            if router2.interfaces.get(i2).address_ipv6_global is None:
                router2.interfaces.get(i2).address_ipv6_global = addresses[1]


'''as.link_dict info comes first from intent file'''
def as_local_links(dict_as):
    for As in dict_as.values():
        for ((r1,i1),(r2,i2)) in As.link_dict.items():
            router1 = get_router_instance(r1,dict_as)
            router2 = get_router_instance(r2,dict_as)
            interface1 = router1.interfaces.get(i1)
            interface2 = router2.interfaces.get(i2)
            
            router1.all_interfaces[interface1.name] = 1 #same as below but more clear
            interface1.statu = "up" # need to be associated by corresponding Cisco command
            interface1.connected_router = router2.router_id
            interface1.connected_interface = interface2.name
            router1.neighbors.append(router2.router_id)

            router2.all_interfaces[interface2.name] = 1
            interface2.statu = "up" # need to be associated by corresponding Cisco command
            interface2.connected_router = router1.router_id
            interface2.connected_interface = interface1.name
            router2.neighbors.append(router1.router_id)
            
            if router1.position != router2.position:
                interface1.egp_protocol_type = "eBGP"
                interface2.egp_protocol_type = "eBGP"



