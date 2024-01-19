'''
functions that show the results of the analysis, help to test.
'''

def show_as_router_status(As):
    print("AS",As.as_id,"router status: ")
    for router in As.routers.values():
        for interface in router.interfaces.values():
            print(router.router_id,":",interface.name,'"igp: ',interface.igp_protocol_type, "@process:",interface.protocol_process)
            print(router.router_id,":",interface.name,'"egp: ',interface.egp_protocol_type)
        print("")

def show_as_router_address(As):
    print("AS",As.as_id,"address plan:")
    for router in As.routers.values():
        for interface in router.interfaces.keys(): #interface as a string
            print(router.router_id,":",interface,':',router.interfaces[interface].address_ipv6_global)
        print(" ")

def show_as_loopback_plan(As):
    print("AS",As.as_id,"loopback plan:")
    for router in As.routers.values():
        print(router.router_id,":",router.loopback)
    print("")