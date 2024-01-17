"""
reg is a object of class output
"""


"""
Implement the protocol RIP
"""
def as_enable_rip(As,reg):  
    process_id = 1 
    order = 3
    for router in As.routers.values():
        reg.write(router.router_id,order,"ipv6 router rip "+str(process_id))
        reg.write(router.router_id,order," redistribute connected")
        
        for interface in router.interfaces.values():
            if interface.protocol_type == "OSPF":
                raise Exception("RIP and OSPF cannot be enabled at the same time")
            if interface.statu == "up" and interface.protocol_type == None:
                interface.protocol_type = "RIP"
                interface.protocol_process = process_id      
                #Cisco: ipv6 rip process_id enableS
                reg.write(router.router_id, interface.name,"ipv6 rip "+str(process_id)+" enable")
        reg.write(router.router_id,"Loopback0","ipv6 rip "+str(process_id)+" enable")
        
        

"""
Implement the protocol OSPF
"""
def as_enable_ospf(As,reg):
    process_id = 2 #different from RIP
    order = 3
    for router in As.routers.values():
        reg.write(router.router_id,order,"ipv6 router ospf "+str(process_id))
        reg.write(router.router_id,order," router-id "+router.router_id)
        reg.write(router.router_id,order," log-adjacency-changes")
        for interface in router.interfaces.values(): #interface as an object
            if interface.protocol_type == "eBGP":             
                # Cisco: ''passive-interface %interface_name
                reg.write(router.router_id, order," passive-interface "+interface.name)
        reg.write(router.router_id,order," !")
        
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
For all ABR in all as, mark their ebgp interface and find the info of its connected int. RETURN: {(as,router,ABR_interface,@int):(as,router,ABR_interface,@int)}
可能要得到连接路由器as的role
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
                    
                    ABR_int_address1 = dict_routers[r1].interfaces.get(int1).address_ipv6_global
                    ABR_int_address2 = dict_routers[r2].interfaces.get(int2).address_ipv6_global
                    
                    neighbor_info[(dict_routers[r1].position,r1,int1,ABR_int_address1)] = (dict_routers[r2].position,r2,int2,ABR_int_address2)
                    neighbor_info[(dict_routers[r2].position,r2,int2,ABR_int_address2)] = (dict_routers[r1].position,r1,int1,ABR_int_address1)
    return neighbor_info

'''
For one particular ABR, find the info of its ebgp interface. RETURN: (as,router,ABR_interface,@int)
'''     
def find_eBGP_neighbor_info(r,int,neighbor_info): #int(str) = interface.name
    for key,value in neighbor_info.items():
        if key[1] == r and key[2]==int:
            return value
    return('not found')

"""
Implement the protocol BGP
"""
def as_enable_BGP(dict_as, loopback_plan, neighbor_info, reg,  apply_policy=False):
    #加快运行速度：不是反复执行相同的boucle以保证指令顺序而是在输出列表里每条消息前加一个顺序指示符，并在最终的输出时排序
    # loopback_plan: result of distribute_loopback(dict_as)
    # neighbor_info: result of generate_eBGP_neighbor_info(dict_as)
    order = 1
    for As in dict_as.values():
        for router in As.routers.values(): #router as an object
            #Cisco: router bgp %as_id， 
            #'' bgp router-id %router_id, 
            #'' no bgp default ipv4-unicast,
            #'' bgp log-neighbor-changes
            reg.write(router.router_id,order,"router bgp "+str(As.as_id))
            reg.write(router.router_id,order," bgp router-id "+router.router_id)
            reg.write(router.router_id,order," no bgp default ipv4-unicast")
            reg.write(router.router_id,order," bgp log-neighbor-changes")

            for loopback in loopback_plan.values():
                if loopback != router.loopback:
                    #Cisco: neighbor %loopback remote-as %as_id
                    #'' neighbor %loopback update-source %interface 
                    reg.write(router.router_id,order," neighbor "+str(loopback)+" remote-as "+str(router.position)) 
                    reg.write(router.router_id,order," neighbor "+str(loopback)+" update-source loopback0")

            for interface in router.interfaces.values(): #interface as an object
                if interface.protocol_type == "eBGP": #对于每个ebgp接口
                    (rm_as,_,_,ABR_int_address) = find_eBGP_neighbor_info(router.router_id,interface.name,neighbor_info) 
                    #Cisco: neighbor %interface.address_ipv6_global remote-as %neighbor_as_id
                    reg.write(router.router_id,order," neighbor "+ABR_int_address+" remote-as "+str(rm_as))
            
            reg.write(router.router_id,order,"!")
            reg.write(router.router_id,order,"address-family ipv6")
            
            for loopback in loopback_plan.values():
                if loopback != router.loopback:
                    # copie '' neighbor %loopback remote-as %as_id and replace "remote-as..." with "activate"
                    reg.write(router.router_id,1," neighbor "+str(loopback)+" activate") 
                    if apply_policy:
                        reg.write(router.router_id,1," neighbor "+str(loopback)+" send-community")           
        
            for interface in router.interfaces.values(): #对于每个ebgp接口
                if apply_policy and interface.protocol_type == "eBGP":
                    reg.write(router.router_id,order," neighbor "+str(interface.address_ipv6_global)+" activate")
                    reg.write(router.router_id,order," neighbor "+str(interface.address_ipv6_global)+" route-map TAG_COMMUNITY in")
                    reg.write(router.router_id,order," neighbor "+str(interface.address_ipv6_global)+" route-map FILTER_COMMUNITY out")
                    # 单独写
            for interface in router.interfaces.values(): #对于每个启用的接口  
                if interface.statu == "up":
                #Cisco: '' network %interface.address_ipv6_global /mask 
                    reg.write(router.router_id,order," network "+str(interface.address_ipv6_global)+str('/64'))
            
            reg.write(router.router_id,order," redistribute connected route-map SET_COMMUNITY")
            process = 1 if As.igp == "RIP" else 2
            reg.write(router.router_id,order," redistribute "+ As.igp.lower() + " "+ str(process) +" route-map SET_COMMUNITY")
            #Cisco: '' exit-address-family
            #!
            reg.write(router.router_id,order," exit-address-family")
            reg.write(router.router_id,order,"!")

'''
functions related to output
'''
def as_config_interfaces(dict_as,reg):
    for As in dict_as.values():
        for router in As.routers.values():
            for interface in router.interfaces.values():
                if interface.statu == "up":
                    reg.write(router.router_id,interface.name,"no ip address")
                    reg.write(router.router_id,interface.name,"negotiation auto")
                    reg.write(router.router_id,interface.name,"ipv6 address "+str(interface.address_ipv6_global)+str('/64'))

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


"""
functions related to rooting policies
"""

def create_community_list(r, int, route_map_name, community_num, reg): #route_map_name: str
    order = 2
    reg.write(r,order,"ip community-list standard "+route_map_name+" permit "+str(community_num))
    reg.log[r][int]["route_map_name"] = route_map_name

def create_prefix_list(r, int, route_map_name, seq_num, reg):
    order = 4
    reg.write(r,order,"ip prefix-list "+route_map_name+" seq "+seq_num+" permit ::/0 le 128")
    reg.log[r][int]["route_map_name"] = route_map_name

def create_route_map(r, route_map_name, seq_num, community_num, action, reg):
    order = 5
    if  "TAG_COMMUNITY" in action:
        reg.write(r,order,"route-map " + action + " permit " + seq_num)
        reg.write(r,order,"match ipv6 address prefix-list "+ route_map_name)
        
        localpref = {"provider":100,"settlement-free peer":200,"customer":300}
        reg.write(r,order,"set local preference " + str(localpref["?"]))#?需要获得信息，连接的as的community
        reg.write(r,order,"set community " + str(community_num)+" additive")

    elif "SET_COMMUNITY" in action:
        reg.write(r,order,"route-map " + action + " permit " + str(seq_num))
        reg.write(r,order,"set community " + str(community_num)+" additive")
        reg.write(r,order,"!")
    
    elif "FILTER_COMMUNITY" in action:
        reg.write(r,order,"route-map "+route_map_name+" permit "+str(seq_num))
        reg.write(r,order," match community "+route_map_name)
        reg.write(r,order,"!")
        reg.write(r,order,"route-map "+route_map_name+" deny "+str(seq_num+10))


# def apply_policy(router,reg):#router as an object
#     N = 5 # maximal number of as that the router can connect to
#     taglst = []
#     setlst = []
#     filterlst = []
#     for i in range(N):
#         taglst.append("TAG_COMMUNITY"+str(i))
#         setlst.append("SET_COMMUNITY"+str(i))
#         filterlst.append("FILTER_COMMUNITY"+str(i))



