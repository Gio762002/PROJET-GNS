import class_reseau as cr
'''
Clarification : all full names (router/interface) refer to objects, and all abbrev refer to strings 
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
def delete_link(router1,router2,as_lst): # = reset_interface for both sides
    for interface in router1.interfaces.values():
        if interface.connected_router == router2.router_id:
            reset_interface(router1,interface.name)
    for interface in router2.interfaces.values():
        if interface.connected_router == router1.router_id:
            reset_interface(router2,interface.name)
    # uploade the AS link list
    for As in as_lst:
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
def get_router_object(router_id,as_lst):
    for As in as_lst:
        if router_id in As.routers.keys():
            return As.routers.get(router_id)
    raise Exception("router_id not found")

def as_auto_addressing_for_link(As,ip_range,as_lst): # ip_range = "2001:100::0", AS as an object, As_lst as a list of AS objects
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
            router1 = get_router_object(r1,as_lst)
            router2 = get_router_object(r2,as_lst)
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


'''对所有AS中的所有ABR,找到其ebgp端口连接的ASBR的信息 输出为一个字典{(as,router,ABR_interface):(as,router,ABR_interface)}'''
def eBGP_neighbour_info(lst_as): 
    neighbour_info = {}
    for As in lst_as:
        for router_id,router in As.routers.items():
            for interface in router.interfaces.values():
                if interface.protocol_type == "eBGP":
                    for As2 in lst_as, As2.as_id != As.as_id:
                        for router_id2,router2 in As2.routers.items():
                            for interface2 in router2.interfaces.values(), interface2.protocol_type == "eBGP":
                                if interface2.connected_router == router_id:
                                    neighbour_info[(As.as_id,router_id,interface.name)] = (As2.as_id,router_id2,interface2.name)
                                #same link will be added twice, but it doesn't matter
    return neighbour_info
'''对于一个ABR,找到其ebgp端口连接的ASBR的信息 输出为一个字典{(as,router,ABR_interface):(as,router,ABR_interface)}'''     
def find_eBGP_neighbour_info(int,lst_as): #int(str) = interface.name
    neighbour_info = eBGP_neighbour_info(lst_as)
    for key,value in neighbour_info.items():
        if key[2]==int:
            return value
