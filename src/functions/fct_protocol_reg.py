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
    RETURN: {(as,router,ABR_interface,@int):(as,router,ABR_interface,@int)}
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
                    
                    neighbor_info[(dict_routers[r1].position,r1,int1,ABR_int_address1)] = (dict_routers[r2].position,r2,int2,ABR_int_address2)
                    neighbor_info[(dict_routers[r2].position,r2,int2,ABR_int_address2)] = (dict_routers[r1].position,r1,int1,ABR_int_address1)
    return neighbor_info

   
def find_eBGP_neighbor_info(r,int,neighbor_info): #int(str) = interface.name
    '''
    For one particular ABR, find the info of its ebgp interface. RETURN: (As,router,ABR_interface,@int)
    '''  
    for key,value in neighbor_info.items():
        if key[1] == r and key[2]==int:
            return value
    return('not found')

def find_As_neighbor(As,dict_as):
    """find all the As neighbors of an As from its link_dict. RETURN: {r.id : (As.community, As.community_number)}"""
    As_neighbor = {}
    for (r1,_),(r2,_) in As.link_dict.items(): # find router r2, that is not in the As but connected to it
        if r2 not in As.routers.keys():
            for As2 in dict_as.values():
                if r2 in As2.routers.keys(): # find the As where the router is located
                    As_neighbor[r1] = (As2.community, As2.community_number)
        elif r1 not in As.routers.keys():
            for As2 in dict_as.values():
                if r1 in As2.routers.keys():
                    As_neighbor[r2] = (As2.community, As2.community_number)
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
                    (rm_as,_,_,ABR_int_address) = find_eBGP_neighbor_info(router.router_id,interface.name,neighbor_info) 
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
        connected_As_info = find_As_neighbor(As, dict_as) 
        for router in As.routers.values():
            if router.router_id in connected_As_info.keys(): # this router is an ABR
                As2_infos = connected_As_info[router.router_id] #{r : (As.community, As.community_number)}

                reg.write(router.name, 4, "route-map ROUTE-MAP-IN permit " + str(10))
                if As2_infos[0] == "customer": # tag community only for ABR connected to customer
                    cus_as_id = As2_infos[1]
                    reg.write(router.name, 4, " match ipv6 address prefix-list LIST-CUSTOMER")
                    reg.write(router.name, 3, "ipv6 prefix-list LIST-CUSTOMER seq " + str(10) + " permit ::/0 le 128")
                    reg.write(router.name, 4, " set community " + str(cus_as_id) + " additive")
                
                reg.write(router.name, 3, "!")
                reg.write(router.name, 3, "!")

                localpref = {"provider":100, "settlement-free peer":200, "customer":300}
                reg.write(router.name, 4, " set local-preference " + str(localpref[As2_infos[0]])) # set local-pref for all ABR
                
                for interface in router.interfaces.values():
                    if interface.egp_protocol_type == "eBGP":
                        connected_address = find_eBGP_neighbor_info(router.router_id, interface.name, neighbor_info)[3]
                        reg.write(router.name, 1, "  neighbor " + str(connected_address) + " route-map ROUTE-MAP-IN in","g") 
                        if As2_infos[0] == "settlement-free peer": # permit customer tag
                            filter_community(router.name, "LIST-CUSTOMER-OUT", "ROUTE-MAP-OUT", cus_as_id, reg)
                            reg.write(router.name, 1, "  neighbor " + str(connected_address) + " route-map ROUTE-MAP-OUT OUT","g")          
            for loopback in As.loopback_plan.values():
                if loopback != router.loopback:
                    reg.write(router.name, 1, "  neighbor " + str(loopback)[:-4] + " send-community","f")   

def filter_community(r, list_name, route_map, community_num, reg):
    reg.write(r, 1, "ip community-list standard " + list_name + " permit " + str(community_num),"k")
    reg.write(r, 4, "!")
    reg.write(r, 4, "!")
    reg.write(r, 4, "route-map " + route_map + " permit " + str(10))
    reg.write(r, 4, " match community " + list_name)
    reg.write(r, 4, "!")
    reg.write(r, 4, "route-map " + route_map + " deny " + str(20))

        # if 连接的as == customer
            # 进： tag 这个r 上的路由
        # 其他abr ：
            #如果连接的是 peer
                # 出： permit 这个tag ， deny所有其他的
            # 如果是provider
                # pass
# def as_config_propagate_cus(dict_as, neighbor_info, reg):
#         for As in dict_as.values():
#             connected_As_info = find_As_neighbor(As, dict_as) # {r.id : (As.community, As.community_number)}
#             for router in As.routers.values():
#                 if router.router_id in connected_As_info.keys(): # this router is an ABR
#                     if connected_As_info[router.router_id][0] == "customer":  # this router connects to a customer As
#                         for interface in router.interfaces.values():
#                             if interface.egp_protocol_type == "eBGP":
#                                 (as_id, _, _, address_int) = find_eBGP_neighbor_info(router.router_id, interface.name, neighbor_info)
#                                 print(as_id, _, _, address_int)
#                                 if dict_as.get(f"as{as_id}").community == "customer":
#                                     reg.write(router.name, 1, "  neighbor " + str(address_int) + " route-map TAG-CUSTOMER in","g")

#             for r,(commu,_) in connected_As_info.items():
#                 if commu == "settlement-free peer":
#                     for router in As.routers.values():
#                         if router.router_id == r:
#                             r_name = router.name
#                     filter_community(r_name, "CUSTOMER-IN", "TAG-CUSTOMER", reg)