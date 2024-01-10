import class_reseau as classr
import fct_reseau as fctr


"""
Implement the protocol RIP
"""
def as_enable_rip(As): 
    process_counter = {} # {rt:process counter}
    for ((rt1,int1),(rt2,_)) in As.link_dict.items():
        process_counter[rt1] = 0 if rt1 not in process_counter.keys() else process_counter[rt1]
        if rt1 in As.routers.keys() and rt2 in As.routers.keys(): #except ABR,ASBR
            router = As.routers.get(rt1)
            interface = router.interfaces.get(int1)
            if interface.protocol_type == None:
                process_counter[rt1] += 1
                interface.protocol_type = "RIP"
                interface.protocol_process = process_counter[rt1] #Cisco: ipv6 rip process_id enable (except ABR,ASBR)


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

'''对所有AS中的所有ABR,标记ebgp端口,找到其连接的ASBR的信息 输出为一个字典{(as,router,ABR_interface):(as,router,ABR_interface)}'''            
def generate_eBGP_neighbour_info(dict_as):
    neighbour_info = {}
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
                    neighbour_info[(dict_routers[r1].position,r1,int1)] = (dict_routers[r2].position,r2,int2)
                    neighbour_info[(dict_routers[r2].position,r2,int2)] = (dict_routers[r1].position,r1,int1)
    return neighbour_info


'''对于一个ABR,找到其ebgp端口连接的ASBR的信息 输出为(as,router,ABR_interface)'''     
def find_eBGP_neighbour_info(rt,int,neighbour_info): #int(str) = interface.name
    for key,value in neighbour_info.items():
        if key[1] == rt and key[2]==int:
            return value
    return('not found')

"""
Implement the protocol BGP
"""
def as_enable_BGP(dict_as, loopback_plan):# loopback_plan: result of fctr.distribute_loopback(dict_as)
    neighbour = generate_eBGP_neighbour_info(dict_as)
    for As in dict_as.values():
        print("considering AS:",As.as_id)
        for router in As.routers.values(): #router as an object
            #Cisco: router bgp %as_id， 
            #'' bgp router-id %router_id, 
            #'' no bgp default ipv4-unicast,
            #'' bgp log-neighbor-changes
            print('considering router:',router.router_id)
            for interface in router.interfaces.values(): #interface as an object
                if interface.protocol_type == "eBGP":
                    print("get eBGP interface:",interface.name)
                    # (remote_as,connected_rt,connected_int)=find_eBGP_neighbour_info(router.router_id,interface.name,neighbour)
                    print("$$$",find_eBGP_neighbour_info(router.router_id,interface.name,neighbour))
                    # print("Ciscotype1:",remote_as,':',connected_rt,":",connected_int)
                    
                    #Cisco: neighbor %interface.address_ipv6_global remote-as %neighbour_as_id
                else:
                    for loopback in loopback_plan.values():
                        if loopback != router.loopback:
                            print("Ciscotype2:",loopback)
                            
                        #Cisco: neighbor %loopback remote-as %as_id
                        #'' neighbor %loopback update-source %interface                
            #!
            #address-family ipv6
            #copie '' neighbor %loopback remote-as %as_id and replace "remote-as..." with "activate"
            for interface in router.interfaces.values():
                #Cisco: '' network %interface.address_ipv6_global /mask 
                print("Ciscotype3:",interface.address_ipv6_global)
                
            #Cisco: '' exit-address-family
            #!