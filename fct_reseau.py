import class_reseau as cr

def init_interface(router,interface):
    router.all_interfaces[interface.name] = 0
    router.interfaces[interface.name] = interface

def set_interface(router, interface,connected_router,connected_interface):
    router.all_interfaces[interface] = 1
    (router.interfaces[interface]).statu = "up" # need to be associated by corresponding Cisco command
    (router.interfaces[interface]).connected_router = connected_router
    router.interfaces[interface].connected_interface = connected_interface

def find_available_interface(all_interfaces):
    try:
        for interface, status in all_interfaces.items():
            if status == 0:
                return interface
        raise Exception("No available interface found.")
    except Exception as e:
        print(e)

def local_link(router1,router2,address1,address2):
    # for each router, find a free interface  
    interface1 = find_available_interface(router1.all_interfaces)
    interface2 = find_available_interface(router2.all_interfaces)
    
    # connect the two interfaces
    set_interface(router1,interface1,router2,interface2)
    set_interface(router2,interface2,router1,interface1)
    router1.neighbours.append(router2.router_id)
    router2.neighbours.append(router1.router_id)

    #distribute ipv6 address
    router1.interfaces[interface1].address_ipv6_global = address1 # distribution automatique realised in main.py
    router2.interfaces[interface2].address_ipv6_global = address2

def reset_interface(router,interface):
    router.all_interfaces[interface] = 0
    router.interfaces[interface].statu = "down"
    router.interfaces[interface].connected_router = None
    router.interfaces[interface].connected_interface = None

def reinit_router(router,loopback,type):
    router.loopback = loopback
    router.type = type

def reinit_as(AS,id,igp):
    AS.as_id = id
    AS.igp = igp
 
def add_router_to_as(router,AS):
    AS.routers[router.router_id] = router

def add_router_to_graph(router,AS):
    AS.graph[router.router_id] = router.neighbours


def as_auto_addressing(AS,ip_range,numero_link): # ip_range = "2001:100::0"
    for router_id,router in AS.routers.items():
        number = 0
        for interface in router.interfaces.values():
            number += 1
            if interface.address_ipv6_global == None:
                interface.address_ipv6_global = ip_range + str(AS.number) + ":" + str(numero_link) + ":" + str(number)         