import class_reseau as cr

def init_interface(router,interface):
    router.all_interfaces[interface.name] = 0 # .name is the key
    router.interfaces[interface.name] = interface

def set_interface(router1, interface1,router2,interface2):#interface as a string
    router1.all_interfaces[interface1] = 1 #same as below but more clear
    router1.interfaces[interface1].statu = "up" # need to be associated by corresponding Cisco command
    router1.interfaces[interface1].connected_router = router2.router_id
    router1.interfaces[interface1].connected_interface = interface2
    router1.neighbours.append(router2.router_id)

    router2.all_interfaces[interface2] = 1
    router2.interfaces[interface2].statu = "up" # need to be associated by corresponding Cisco command
    router2.interfaces[interface2].connected_router = router1.router_id
    router2.interfaces[interface2].connected_interface = interface1
    router2.neighbours.append(router1.router_id)


def find_available_interface(all_interfaces):
    try:
        for interface, status in all_interfaces.items():
            if status == 0:
                return interface # return the name of the interface
        raise Exception("No available interface found.")
    except Exception as e:
        print(e)

'''need find_available_interface, set_interface'''
def local_link(router1,router2):
    # for each router, find a free interface  
    interface1 = find_available_interface(router1.all_interfaces) # interface as a string
    interface2 = find_available_interface(router2.all_interfaces)
    # connect the two interfaces
    set_interface(router1,interface1,router2,interface2)
    # #distribute ipv6 addresses
    # router1.interfaces[interface1].address_ipv6_global = address1 # automatic distribution realised in main.py
    # router2.interfaces[interface2].address_ipv6_global = address2

def reset_interface(router,interface): # only one side
    router.all_interfaces[interface] = 0
    router.interfaces[interface].statu = "down"
    router.interfaces[interface].connected_router = None
    router.interfaces[interface].connected_interface = None

'''need reset_interface'''
def delete_link(router1,router2): # = reset_interface for both sides
    for interface in router1.interfaces.values():
        if interface.connected_router == router2.router_id:
            reset_interface(router1,interface.name)
    for interface in router2.interfaces.values():
        if interface.connected_router == router1.router_id:
            reset_interface(router2,interface.name)

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


'''three fcts concerning address distribution'''
#distribution of ipv6 addresses for 2 interfaces connected to each other
def as_auto_addressing(AS,ip_range,interface1,interface2,numero_link): # ip_range = "2001:100::0", AS as an object, interface as a string
        if interface1 == AS.link_lst[numero_link][0][1] and interface2 == AS.link_lst[numero_link][1][1]:
            address1 = ip_range + str(AS.as_id) + ":" + str(numero_link) + "::1"
            address2 = ip_range + str(AS.as_id) + ":" + str(numero_link) + "::2"
            # if AS.link_lst[numero_link][0][0] > AS.link_lst[numero_link][1][0]:
            #     return (address2,address1)
            # else:
            return (address1,address2)# router having bigger id has bigger address
        

def as_auto_loopback(AS,ip_range): # AS as an object
    for router_id,router in AS.routers.items():
        router.loopback = ip_range + str(AS.as_id) + ":" + (str(router_id).split('.'))[0] + "::1/128"
        loopback_interface = find_available_interface(router.all_interfaces)
        router.loopback_interface = loopback_interface # interface as a string
        router.all_interfaces[loopback_interface] = 1
        router.interfaces[loopback_interface].statu = "up"
        router.interfaces[loopback_interface].address_ipv6_global = router.loopback
        router.interfaces[loopback_interface].tag = 1 

def as_loopback_plan(AS): #AS as an object
    for router_id,router in AS.routers.items():
        AS.loopback_plan[router_id] = router.loopback


'''对于一个ABR,找到其ebgp端口连接的ASBR的信息 输出为一个字典{(as,router,ABR_interface):(as,router,ABR_interface)}'''
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
        
def find_eBGP_neighbour_info(interface,lst_as): #interface(str) = interface.name
    neighbour_info = eBGP_neighbour_info(lst_as)
    for key,value in neighbour_info.items():
        if key[2]==interface:
            return value
