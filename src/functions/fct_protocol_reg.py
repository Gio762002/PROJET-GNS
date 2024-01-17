"""
reg is a object of class output
"""


"""
Implement the protocol RIP
"""
def as_enable_rip(As,reg):  
    process_id = 1 
    for ((rt1,int1),(rt2,_)) in As.link_dict.items():
        if rt1 in As.routers.keys() and rt2 in As.routers.keys(): #except ABR,ASBR
            router = As.routers.get(rt1)
            interface = router.interfaces.get(int1)
            if interface.protocol_type == "OSPF":
                raise Exception("RIP and OSPF cannot be enabled at the same time")
            if interface.protocol_type == None:
                interface.protocol_type = "RIP"
                interface.protocol_process = process_id      
                #Cisco: ipv6 rip process_id enable
                reg.write(rt1, interface.name,"ipv6 rip "+str(process_id)+" enable")
    for router in As.routers.values():
        reg.write(router.router_id,"Loopback0","ipv6 rip "+str(process_id)+" enable")


"""
Implement the protocol OSPF
"""
def as_enable_ospf(As,reg):
    process_id = 2 #different from RIP
    for router in As.routers.values():
        for interface in router.interfaces.values(): #interface as an object
            if interface.protocol_type == "eBGP":             
                # Cisco: ''passive-interface %interface_name
                reg.write(router.router_id, interface.name," passive-interface "+interface.name)

        for interface in router.interfaces.values():
            if interface.protocol_type == "RIP":
                raise Exception("RIP and OSPF cannot be enabled at the same time")
            if interface.statu == "up" and interface.protocol_type == None:
                interface.protocol_type = "OSPF"
                interface.protocol_process = process_id      
                #Cisco: ipv6 ospf %process_id area %area_idd
                reg.write(router.router_id, interface.name,"ipv6 ospf "+str(process_id)+" area "+str(router.position))
        reg.write(router.router_id,"Loopback0","ipv6 ospf "+str(process_id)+" area "+str(router.position))

'''
For all ABR in all as, mark their ebgp interface and find the info of its connected int. RETURN: {(as,router,ABR_interface):(as,router,ABR_interface)}
'''            
def generate_eBGP_neighbor_info(dict_as):
    neighbor_info = {}
    #this part generates a dict of all router objects, which to be used to get easily the router object by its id
    #if this part will be used frequently, it is better to put it in a separate function
    dict_routers = {}
    for As in dict_as.values():
        for router_id,router in As.routers.items():
            dict_routers[router_id] = router
    
    for As in dict_as.values():
        for (r1,int1),(r2,int2) in As.link_dict.items(): # same infomation will be viewed 4 times, a little bit waste
            if As.routers.get(r1) == None or As.routers.get(r2) == None: #means interconnection with other AS
                if dict_routers[r1].interfaces.get(int1).protocol_type == None: # reduce the 4-time waste to 1-time waste ?
                    dict_routers[r1].interfaces.get(int1).protocol_type = "eBGP"
                    dict_routers[r2].interfaces.get(int2).protocol_type = "eBGP" #mark the interface as eBGP
                    neighbor_info[(dict_routers[r1].position,r1,int1)] = (dict_routers[r2].position,r2,int2)
                    neighbor_info[(dict_routers[r2].position,r2,int2)] = (dict_routers[r1].position,r1,int1)
    return neighbor_info

'''
For one particular ABR, find the info of its ebgp interface. RETURN: (as,router,ABR_interface)
'''     
def find_eBGP_neighbor_info(rt,int,neighbor_info): #int(str) = interface.name
    for key,value in neighbor_info.items():
        if key[1] == rt and key[2]==int:
            return value
    return('not found')

"""
Implement the protocol BGP
"""
def as_enable_BGP(dict_as, loopback_plan, neighbor_info, reg):
    # loopback_plan: result of distribute_loopback(dict_as)
    # neighbor_info: result of generate_eBGP_neighbor_info(dict_as)
    for As in dict_as.values():
        for router in As.routers.values(): #router as an object
            #Cisco: router bgp %as_id， 
            #'' bgp router-id %router_id, 
            #'' no bgp default ipv4-unicast,
            #'' bgp log-neighbor-changes
            reg.write(router.router_id,"general","router bgp "+str(As.as_id))
            reg.write(router.router_id,"general"," bgp router-id "+router.router_id)
            reg.write(router.router_id,"general"," no bgp default ipv4-unicast")
            reg.write(router.router_id,"general"," bgp log-neighbor-changes")

            for loopback in loopback_plan.values():
                if loopback != router.loopback:
                    #Cisco: neighbor %loopback remote-as %as_id
                    #'' neighbor %loopback update-source %interface 
                    reg.write(router.router_id,"general"," neighbor "+str(loopback)+" remote-as "+str(router.position)) 
                    reg.write(router.router_id,"general"," neighbor "+str(loopback)+" update-source loopback0")

            for interface in router.interfaces.values(): #interface as an object
                if interface.protocol_type == "eBGP":
                    (rm_as,_,ABR_interface) = find_eBGP_neighbor_info(router.router_id,interface.name,neighbor_info) 
                    #Cisco: neighbor %interface.address_ipv6_global remote-as %neighbor_as_id
                    reg.write(router.router_id,"general"," neighbor "+ABR_interface+" remote-as "+str(rm_as))
            
            reg.write(router.router_id,"general","!")
            reg.write(router.router_id,"general","address-family ipv6")
            for loopback in loopback_plan.values():
                if loopback != router.loopback:
                    # copie '' neighbor %loopback remote-as %as_id and replace "remote-as..." with "activate"
                    reg.write(router.router_id,"general"," neighbor "+str(loopback)+" activate")            
        
            for interface in router.interfaces.values():
                if interface.statu == "up":
                
                #Cisco: '' network %interface.address_ipv6_global /mask 
                    reg.write(router.router_id,"general"," network "+str(interface.address_ipv6_global)+str('/64'))
                
                
            #Cisco: '' exit-address-family
            #!
            reg.write(router.router_id,"general"," exit-address-family")
            reg.write(router.router_id,"general","!")


def as_config_unused_interface_and_loopback0(dict_as,reg):
    for As in dict_as.values():
        for router in As.routers.values():
            reg.write(router.router_id,"Loopback0","no ip address")
            reg.write(router.router_id,"Loopback0","ipv6 address "+str(router.loopback))
            reg.write(router.router_id,"Loopback0","ipv6 enable")
            
            for interface in router.interfaces.values():
                if interface.statu == "down":
                    #Cisco: interface %interface.name
                    #'' no ipv6 address
                    #'' shutdown
                    #'' negotiation auto
                    #'' !
                    reg.write(router.router_id, interface.name, interface.name)
                    reg.write(router.router_id, interface.name," no ipv6 address")
                    reg.write(router.router_id, interface.name," shutdown")
                    reg.write(router.router_id, interface.name," negotiation auto")
