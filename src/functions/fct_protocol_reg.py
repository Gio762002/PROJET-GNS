"""
reg is an instance of the class 'registrar'. 
It is used to store the configuration commands of routers and interfaces properly in the right position 
whatever the order of calls of the functions. 
"""


def as_enable_rip(As,reg):  
    """Implement RIP for all routers in the As"""
    process_id = 1 
    order = 2
    for router in As.routers.values():
        reg.write(router.name, order, "ipv6 router rip "+str(process_id))
        reg.write(router.name, order, " redistribute connected")
        
        for interface in router.interfaces.values():
            if interface.igp_protocol_type == "OSPF":
                raise Exception("RIP and OSPF cannot be enabled at the same time")
            if interface.statu == "up" and interface.igp_protocol_type == None:
                interface.igp_protocol_type = "RIP"
                interface.protocol_process = process_id      
                reg.write(router.name, interface.name, "ipv6 enable")
                reg.write(router.name, interface.name, "ipv6 rip " + str(process_id) + " enable")
        reg.write(router.name, "Loopback0", "ipv6 rip " + str(process_id) + " enable")
        
        


def as_enable_ospf(As,reg):
    """Implement OSPF for all routers in the As"""
    process_id = 2 #different from RIP
    order = 2
    for router in As.routers.values():
        reg.write(router.name, order, "ipv6 router ospf " + str(process_id))
        reg.write(router.name, order, " router-id " + router.router_id)
        reg.write(router.name, order, " log-adjacency-changes")
        for interface in router.interfaces.values(): 
            if interface.egp_protocol_type == "eBGP":             
                reg.write(router.name, order," passive-interface " + interface.name)
        reg.write(router.name, order, " !")
        
        for interface in router.interfaces.values():
            if interface.igp_protocol_type == "RIP":
                raise Exception("RIP and OSPF cannot be enabled at the same time")
            if interface.statu == "up":
                interface.igp_protocol_type = "OSPF"
                interface.protocol_process = process_id      
                reg.write(router.name, interface.name, "ipv6 enable")
                reg.write(router.name, interface.name, "ipv6 ospf " + str(process_id) + " area 0")
        reg.write(router.name, "Loopback0", "ipv6 ospf " + str(process_id) + " area 0")

         
def generate_eBGP_neighbor_info(dict_as):
    '''
    For all ABR in all as, mark their ebgp interface and find the info of its connected int.
    RETURN: {(as,router,ABR_interface,@int):(as,router_id,ABR_interface,@int,community)}
    可能要得到连接路由器as的role
    '''   
    neighbor_info = {}
    #this part generates a dict of all router objects, which to be used to get easily the router object by its id
    #if this part will be used frequently, it is better to put it in a separate function
    dict_routers = {}
    for As in dict_as.values():
        for router_id,router in As.routers.items():
            dict_routers[router_id] = router
    
    for As in dict_as.values():
        for (r1,int1),(r2,int2) in As.link_dict.items():
            if As.routers.get(r1) == None or As.routers.get(r2) == None: #means interconnection with other AS
                if dict_routers[r1].position != dict_routers[r2].position:
                    
                    ABR_int_address1 = dict_routers[r1].interfaces.get(int1).address_ipv6_global
                    ABR_int_address2 = dict_routers[r2].interfaces.get(int2).address_ipv6_global
                    serve1 = dict_routers[r1].interfaces.get(int1).serve
                    serve2 = dict_routers[r2].interfaces.get(int2).serve
                    
                    neighbor_info[(dict_routers[r1].position, r1, int1, ABR_int_address1, serve1)] = (dict_routers[r2].position, r2, int2, ABR_int_address2, serve2)
                    neighbor_info[(dict_routers[r2].position, r2, int2, ABR_int_address2, serve2)] = (dict_routers[r1].position, r1, int1, ABR_int_address1, serve1)
    return neighbor_info

   
def find_eBGP_neighbor_info(r,int,neighbor_info): #int(str) = interface.name
    '''
    For one particular ABR, find the info of its ebgp interface. RETURN: (As,router,ABR_interface,@int,community)
    '''  
    for key,value in neighbor_info.items():
        if key[1] == r and key[2]==int:
            return value
    return('not found')

def find_As_neighbor(As,dict_as):
    """find all the As neighbors of an As from its link_dict. RETURN: {r.id : [(As.community, As.community_number),..]}"""
    As_neighbor = {}
    for (r1,_),(r2,_) in As.link_dict.items(): # find router r2, that is not in the As but connected to it
        if r2 not in As.routers.keys():
            if As_neighbor.get(r1) is None:
                As_neighbor[r1] = []
            for As2 in dict_as.values():
                if r2 in As2.routers.keys(): # find the As where the router is located
                    As_neighbor[r1].append((As2.community, As2.community_number))
        elif r1 not in As.routers.keys():
            if As_neighbor.get(r2) is None:
                As_neighbor[r2] = []
            for As2 in dict_as.values():
                if r1 in As2.routers.keys():
                    As_neighbor[r2].append((As2.community, As2.community_number))
    if len(As_neighbor) == 0:
        raise Exception("No As neighbor found, the As is isolated")
    return As_neighbor

def as_enable_BGP(dict_as, neighbor_info, reg):
    """
    Implement BGP for all As
    "a","b","c" etc mean the secondary order of writing, this mechanism is particularly designed for BGP, 
    without that, we would have to write 6 loop of only 2 types(interfaces and loopback0)
    """
    order = 1
    for As in dict_as.values():
        for router in As.routers.values():
            def add_exlam(second=None): # add exclamation mark to separate the different parts of the configuration
                if second == None:
                    return reg.write(router.name, order, "!")
                else:
                    return reg.write(router.name, order, "!",second)
        
            reg.write(router.name, order, "router bgp " + str(As.as_id),"a")
            reg.write(router.name, order, " bgp router-id " + router.router_id,"a")
            reg.write(router.name, order, " no bgp default ipv4-unicast","a")
            reg.write(router.name, order, " bgp log-neighbor-changes","a")
            reg.write(router.name, order, " !","d")
            reg.write(router.name, order, " address-family ipv6","d")

            for loopback in As.loopback_plan.values():
                if loopback != router.loopback:
                    reg.write(router.name, order, " neighbor " + str(loopback)[:-4] + " remote-as " + str(router.position),"b") 
                    reg.write(router.name, order, " neighbor " + str(loopback)[:-4] + " update-source loopback0","b")

                    reg.write(router.name, order, "  neighbor " + str(loopback)[:-4] + " activate","f")                  
            
            for interface in router.interfaces.values():
                if interface.egp_protocol_type == "eBGP":
                    (rm_as,_,_,ABR_int_address,_) = find_eBGP_neighbor_info(router.router_id,interface.name,neighbor_info) 
                    reg.write(router.name, order, " neighbor " + ABR_int_address + " remote-as " + str(rm_as),"c")
                    reg.write(router.name, order, "  neighbor " + ABR_int_address + " activate","e")
                if interface.statu == "up": 
                    reg.write(router.name, order,  "  network " + str(interface.address_ipv6_global) + str('/64'),"h")
            
            reg.write(router.name, order, " exit-address-family","j")
            add_exlam("j")
            reg.write(router.name, order, "ip forward-protocol nd","j")
            reg.write(router.name, order, "no ip http server","j")
            reg.write(router.name, order, "no ip http secure-server","j")
            add_exlam("j") #"k" is waiting for "ip community-list standard "
            add_exlam("l")
            reg.write(router.name, order, "logging alarm informational","l")
            reg.write(router.name, order, "no cdp log mismatch duplex","l")


'''
functions particularly related to complete the configuration
'''
def as_config_interfaces(dict_as,reg):
    """default config of interfaces of all routers in all As"""
    for As in dict_as.values():
        for router in As.routers.values():
            for interface in router.interfaces.values():
                if interface.statu == "up":
                    reg.write(router.name,interface.name,"no ip address")
                    reg.write(router.name,interface.name,"negotiation auto")
                    reg.write(router.name,interface.name,"ipv6 address "+str(interface.address_ipv6_global)+str('/64'))

def as_config_unused_interface_and_loopback0(dict_as,reg):
    """default config of unused interfaces and loopback0 of all routers in all As"""
    for As in dict_as.values():
        for router in As.routers.values():
            reg.write(router.name,"Loopback0","no ip address")
            reg.write(router.name,"Loopback0","ipv6 address "+str(router.loopback))
            reg.write(router.name,"Loopback0","ipv6 enable")
            
            for interface in router.interfaces.values():
                if interface.statu == "down":
                    reg.write(router.name, interface.name, "no ipv6 address")
                    reg.write(router.name, interface.name, "shutdown")
                    reg.write(router.name, interface.name, "negotiation auto")


"""
function related to rooting policies
"""
def as_config_local_pref(dict_as, neighbor_info, reg):
    """
    Set the local-pref attribute of BGP paths so As to prefer customers over settlement-free peers over providers.
    Tag routes coming from another customer As, and at all routers ABR in itself, only permit the out of routes having this tag if this ABR is connected to peer.
    
    """
    for As in dict_as.values():
        connected_As_info = find_As_neighbor(As, dict_as) #{r:[]}
        # print(As.as_id,"---",connected_As_info)
        for router in As.routers.values():
            if router.router_id in connected_As_info.keys(): # this router is an ABR
                As2_infos_list = connected_As_info[router.router_id] #{r : [(As.community, As.community_number)]}
                
                for As2_infos in As2_infos_list:#(As.community, As.community_number)
                    reg.write(router.name, 4, "route-map "+f"ROUTE-MAP-IN{As2_infos[1]}"+" permit " + str(10),"in")
                    if As2_infos[0] == "customer": # tag community only for ABR connected to customer
                        cus_as_id = As2_infos[1]
                        reg.write(router.name, 4, " match ipv6 address prefix-list LIST-CUSTOMER","in")
                        reg.write(router.name, 3, "ipv6 prefix-list LIST-CUSTOMER seq " + str(10) + " permit ::/0 le 128")
                        reg.write(router.name, 4, " set community " + str(cus_as_id) + " additive","in")
                    if As2_infos[0] == "settlement-free peer": # permit customer tag
                        filter_community(router.name, "LIST-CUSTOMER-OUT", "ROUTE-MAP-OUT", cus_as_id, reg)
                        for interface in router.interfaces.values():
                            if interface.egp_protocol_type == "eBGP":
                                con_add = find_eBGP_neighbor_info(router.router_id, interface.name, neighbor_info)[3]
                                con_serve = find_eBGP_neighbor_info(router.router_id, interface.name, neighbor_info)[4]
                                if con_serve == "settlement-free peer":
                                    reg.write(router.name, 1, "  neighbor " + str(con_add) + " route-map ROUTE-MAP-OUT OUT","g")   
                    reg.write(router.name, 3, "!")
                    reg.write(router.name, 3, "!")

                    localpref = {"provider":100, "settlement-free peer":200, "customer":300}
                    reg.write(router.name, 4, " set local-preference " + str(localpref[As2_infos[0]]),"in") # set local-pref for all ABR
                
                    for interface in router.interfaces.values():
                        if interface.egp_protocol_type == "eBGP":
                            connected_r = interface.connected_router
                            for As in dict_as.values():
                                if connected_r in As.routers.keys():
                                    connected_as_cn = As.community_number # bind int with connected_as_cn
                            connected_address = find_eBGP_neighbor_info(router.router_id, interface.name, neighbor_info)[3]
                            if connected_as_cn == As2_infos[1]:
                                reg.write(router.name, 1, "  neighbor " + str(connected_address) + " route-map "+ f"ROUTE-MAP-IN{As2_infos[1]}"+" in","g")          
            for loopback in As.loopback_plan.values():
                if loopback != router.loopback:
                    reg.write(router.name, 1, "  neighbor " + str(loopback)[:-4] + " send-community","f")   

def filter_community(r, list_name, route_map, community_num, reg):
    '''a function that is seperated from as_config_local_pref()'''
    reg.write(r, 1, "ip community-list standard " + list_name + " permit " + str(community_num),"k")
    reg.write(r, 4, "!","out")
    reg.write(r, 4, "!","out")
    reg.write(r, 4, "route-map " + route_map + " permit " + str(10),"out")
    reg.write(r, 4, " match community " + list_name,"out")
    reg.write(r, 4, "!","out")
    reg.write(r, 4, "route-map " + route_map + " deny " + str(20),"out")

