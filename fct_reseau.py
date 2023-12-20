import class_reseau as cr

def init_interface(router,interface):
    router.all_interfaces[interface.name] = 0 # .name is the key
    router.interfaces[interface.name] = interface

def set_interface(router1, interface1,router2,interface2):
    router1.all_interfaces[interface1.name] = 1 #same as below but more clear
    router1.interfaces[interface1.name].statu = "up" # need to be associated by corresponding Cisco command
    router1.interfaces[interface1.name].connected_router = router2.router_id
    router1.interfaces[interface1.name].connected_interface = interface2.name
    router1.neighbours.append(router2.router_id)

    router2.all_interfaces[interface2.name] = 1
    router2.interfaces[interface2.name].statu = "up" # need to be associated by corresponding Cisco command
    router2.interfaces[interface2.name].connected_router = router1.router_id
    router2.interfaces[interface2.name].connected_interface = interface1.name
    router2.neighbours.append(router1.router_id)


def find_available_interface(all_interfaces):
    try:
        for interface, status in all_interfaces.items():
            if status == 0:
                return interface
        raise Exception("No available interface found.")
    except Exception as e:
        print(e)

'''need find_available_interface, set_interface'''
def local_link(router1,router2,address1,address2):
    # for each router, find a free interface  
    interface1 = find_available_interface(router1.all_interfaces)
    interface2 = find_available_interface(router2.all_interfaces)
    # connect the two interfaces
    set_interface(router1,interface1,router2,interface2)
    #distribute ipv6 address
    router1.interfaces[interface1].address_ipv6_global = address1 # automatic distribution realised in main.py
    router2.interfaces[interface2].address_ipv6_global = address2

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

def reinit_router(router,loopback,type):
    router.loopback = loopback
    router.type = type

#def distribute_router_id(router,numero_router):
#    router.router_id = (str(numero_router)+".")*4-"."

#def reinit_as(AS,id,igp):
#    AS.as_id = id
#    AS.igp = igp
 
def add_router_to_as(router,AS):
    AS.routers[router.router_id] = router


def as_auto_addressing(AS,ip_range,numero_link): # ip_range = "2001:100::0"
    for router_id,router in AS.routers.items():
        number = 0
        for interface in router.interfaces.values():
            number += 1
            if interface.address_ipv6_global == None:
                interface.address_ipv6_global = ip_range + str(AS.number) + ":" + str(numero_link) + ":" + str(number)         

#def auto_loopback(AS,ip_range)

'''need fct to for loopback_plan'''
#def as_loopback_plan(AS):



#def find_neighbour_info(AS): 对于一个ABR，找到其ebgp端口连接的ASBR的信息 输出为一个字典{(as,router,ABR):(as,router,ABR)}
