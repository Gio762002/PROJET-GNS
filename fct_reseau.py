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
            As.update_link_lst(router1.router_id,router2.router_id)


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
#distribution of ipv6 addresses for 2 interfaces connected to each other
def as_auto_addressing_for_link(AS,ip_range,int1,int2,numero_link): # ip_range = "2001:100::0", AS as an object, interface as a string
        if int1 == AS.link_lst[numero_link][0][1] and int2 == AS.link_lst[numero_link][1][1]:
            address1 = ip_range + str(AS.as_id) + ":" + str(numero_link) + "::1"
            address2 = ip_range + str(AS.as_id) + ":" + str(numero_link) + "::2"
            if AS.link_lst[numero_link][0][0] > AS.link_lst[numero_link][1][0]:
                return (address2,address1)
            else:
                return (address1,address2)# router having bigger id has bigger address
        

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
            for interface in router.interfaces.values(), interface.protocol_type == "eBGP":
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
