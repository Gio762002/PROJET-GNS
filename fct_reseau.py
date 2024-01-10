import class_reseau as cr
'''
Clarification : all full names (router/interface) refer to objects, and all abbrev refer to strings 
certains fcts have parameter : lst_as, which is a list of all AS objects that will be used in the main program
'''

def init_interface(router,interface):
    router.all_interfaces[interface.name] = 0 # .name is the key
    router.interfaces[interface.name] = interface

def local_link(router1,router2,interface1,interface2):#all objects
    router1.all_interfaces[interface1.name] = 1 #same as below but more clear
    interface1.statu = "up" # need to be associated by corresponding Cisco command
    interface1.connected_router = router2.router_id
    interface1.connected_interface = interface2.name
    router1.neighbours.append(router2.router_id)

    router2.all_interfaces[interface2.name] = 1
    interface2.statu = "up" # need to be associated by corresponding Cisco command
    interface2.connected_router = router1.router_id
    interface2.connected_interface = interface1.name
    router2.neighbours.append(router1.router_id)

def reset_interface(router,int): # only one side
    router.all_interfaces[int] = 0
    router.interfaces[int].statu = "down"
    router.interfaces[int].connected_router = None
    router.interfaces[int].connected_interface = None
    router.interfaces[int].address_ipv6_global = None

'''need reset_interface'''
def delete_link(router1,router2,lst_as): # = reset_interface for both sides
    for interface in router1.interfaces.values():
        if interface.connected_router == router2.router_id:
            reset_interface(router1,interface.name)
    for interface in router2.interfaces.values():
        if interface.connected_router == router1.router_id:
            reset_interface(router2,interface.name)
    # uploade the AS link list
    for As in lst_as:
        if As.as_id == router1.position or As.as_id == router2.position:
            As.update_link_dict(router1.router_id,router2.router_id)


def reinit_router(router,loopback,type): #router as an object
    router.loopback = loopback
    router.type = type

#def distribute_router_id(router,numero_router):
#    router.router_id = (str(numero_router)+".")*4-"."

#def reinit_as(AS,id,igp):
#    AS.as_id = id
#    AS.igp = igp
 
def add_router_to_as(router,AS): #router,AS are objects
    AS.routers[router.router_id] = router
    router.position = AS.as_id #router.position is a string


'''three fcts concerning address distribution'''
#distribution of ipv6 addresses for an as
def get_router_object(router_id,lst_as):
    for As in lst_as:
        if router_id in As.routers.keys():
            return As.routers.get(router_id)
    raise Exception("router_id not found")

def as_auto_addressing_for_link(As,ip_range,lst_as): # ip_range = "2001:100::0", AS as an object, lst_as as a list of AS objects
        link_dict_copy = As.link_dict.copy()
        numero_link = 0
        for ((r1,i1),(r2,i2)) in As.link_dict.items(): #all are strings   
            del link_dict_copy[(r2,i2)]
            if (r1,i1) in link_dict_copy.keys():
                numero_link += 1
                s_address = ip_range + str(As.as_id) + ":" + str(numero_link) + "::1"
                b_address = ip_range + str(As.as_id) + ":" + str(numero_link) + "::2"
                if r1 > r2:
                    addresses = (b_address,s_address)          
                else:
                    addresses = (s_address,b_address)# router having bigger id has bigger address
            router1 = get_router_object(r1,lst_as)
            router2 = get_router_object(r2,lst_as)
            if router1.interfaces.get(i1).address_ipv6_global is None:
                router1.interfaces.get(i1).address_ipv6_global = addresses[0]
            if router2.interfaces.get(i2).address_ipv6_global is None:
                router2.interfaces.get(i2).address_ipv6_global = addresses[1]

def as_auto_loopback(AS,ip_range): # AS as an object
    for router_id,router in AS.routers.items():
        router.loopback = ip_range + str(AS.as_id) + ":" + (str(router_id).split('.'))[0] + "::1/128"


def as_loopback_plan(AS): #AS as an object
    for router_id,router in AS.routers.items():
        AS.loopback_plan[router_id] = router.loopback




