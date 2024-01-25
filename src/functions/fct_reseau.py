'''
Clarification : all full names (router/interface) refer to instances, and all abbrev refer to strings 
certains fcts have parameter : dict_as, which is a dict of all As instances that will be used in the main program
'''

def init_interface(router,interface):
    """bind interface to router, and add a statu tracker in the attribute 'all_interfaces' (dict): { interface.name : 0/1(occupied?) }"""
    router.all_interfaces[interface.name] = 0 # .name is the key
    router.interfaces[interface.name] = interface

def add_router_to_as(router,As): 
    """bind router to As, and update router.position to As.as_id, which is a string"""
    As.routers[router.router_id] = router
    router.position = As.as_id 


'''
Three fcts of distribution of addresses
'''
def get_router_instance(router_id,dict_as):
    """distribution of ipv6 addresses for an As"""
    for As in dict_as.values():
        if router_id in As.routers.keys():
            return As.routers.get(router_id)
    raise Exception("router_id not found")

def as_auto_addressing_for_link(dict_as):
    """distribution of ipv6 addresses for an As, based on the links the routers in the As have"""
    for As in dict_as.values():    
        link_dict_copy = As.link_dict.copy()
        numero_link = 0
        for ((r1,i1),(r2,i2)) in As.link_dict.items(): #all are strings   
            if (r2,i2) in link_dict_copy.keys():
                del link_dict_copy[(r2,i2)] # eliminate the reverse link to avoid duplicate
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


def connect_routers(router1, interface1, router2, interface2):
    """separated from the function below for making the code more readable"""
    router1.all_interfaces[interface1.name] = 1
    interface1.statu = "up"
    interface1.connected_router = router2.router_id
    interface1.connected_interface = interface2.name
    if router2.router_id not in router1.neighbors:
        router1.neighbors.append(router2.router_id)

def as_local_links(dict_as):
    '''It might be confusing that As.link_dict comes before the execution of this function, 
    in fact, as.link_dict infos come first from intent file in the main program, and this attribute contains only verbal descriptions of links,
    this function is to make the links 'real' and trackable by updating the attributes of the interfaces'''
    for As in dict_as.values():
        for ((r1,i1),(r2,i2)) in As.link_dict.items():
            router1 = get_router_instance(r1,dict_as)
            router2 = get_router_instance(r2,dict_as)
            interface1 = router1.interfaces.get(i1)
            interface2 = router2.interfaces.get(i2)
            connect_routers(router1, interface1, router2, interface2)
            connect_routers(router2, interface2, router1, interface1)
            
            if router1.position != router2.position:
                interface1.egp_protocol_type = "eBGP"
                interface2.egp_protocol_type = "eBGP"


# functions not used in our program, but are valuable for future use
def reset_interface(router,int):
    """reset an interface to its initial state, if ever there is a need to change the topology"""
    router.all_interfaces[int] = 0
    router.interfaces[int].statu = "down"
    router.interfaces[int].connected_router = None
    router.interfaces[int].connected_interface = None
    router.interfaces[int].address_ipv6_global = None

def delete_link(router1,router2,dict_as): 
    """== reset_interface for both sides of a link"""
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