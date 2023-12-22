import class_reseau as classr
import fct_reseau as fctr


"""
Implement the protocol RIP
"""
def set_rip(router, process_id): #Cisco: ipv6 rip process_id enable
    for interface in router.interfaces.values():
        if interface.statu == "up":
            interface.protocol_type = "RIP"
            interface.protocol_process = process_id


"""
Implement the protocol OSPF
"""
def set_ospf(router, process_id): #Cisco: ipv6 router ospf %process_id
    # ''router_id %router.router_id
    # ''log-adjaency-changes
    for interface in router.interfaces.values(): #interface as an object
        if interface.protocol_type == "eBGP": 
            pass # Cisco: ''passive-interface %interface_name
    for interface in router.interfaces.values():
        if interface.statu == "up":
            interface.protocol_process = process_id #Cisco: ipv6 ospf %process_id area %area_id
            

"""
Implement the protocol BGP
"""
def set_BGP(lst_as, loopback_plan):# loopback_plan: result of fctr.distribute_loopback(lst_as)
    for As in lst_as:
        for router in As.routers.values(): #router as an object
            #Cisco: router bgp %as_id， 
            #'' bgp router-id %router_id, 
            #'' no bgp default ipv4-unicast,
            #'' bgp log-neighbor-changes
            for interface in router.interfaces.values(): #interface as an object
                if interface.protocol_type == "eBGP":
                    (remote_as,connected_router,connected_interface)=fctr.find_eBGP_neighbour_info(interface.name, lst_as)
                    pass
                    #Cisco: neighbor %interface.address_ipv6_global remote-as %neighbour_as_id
                else:
                    for loopback in loopback_plan:
                        if loopback != router.loopback:
                            pass
                        #Cisco: neighbor %loopback remote-as %as_id
                        #'' neighbor %loopback update-source %interface                
            #!
            #address-family ipv6
            #copie '' neighbor %loopback remote-as %as_id and replace "remote-as..." with "activate"
            for interface in router.interfaces.values():
                #Cisco: '' network %interface.address_ipv6_global /mask 
                pass
            #Cisco: '' exit-address-family
            #!