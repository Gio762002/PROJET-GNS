class router:
   
    def __init__(self,name,type="Internal"):
        self.name = name
        self.router_id = None
        self.loopback = None
        self.all_interfaces = {"Loopback0":1} #interface.name : occupied? (1 or 0)
        #self.routing_table = {} ##maybe not needed
        self.interfaces = {} #interface.name: interface(object)
        self.neighbors = [] #router_id, extrait de self.interface
        self.type = type # ABR, ASBR, Internal 
        self.position = None # name of the AS where the router is located, to be tracked for any modification 

class interface:
    
    def __init__(self,name,igp_protocol_type=None):
        self.name = name # !!! can be the same with other interfaces of other routers
        self.statu = "down" # up or down
        self.address_ipv6_global = None
        self.netmask = None
        self.connected_router = None # router_id
        self.connected_interface = None # interface.name
        self.igp_protocol_type = igp_protocol_type
        self.egp_protocol_type = None   
        self.protocol_process = None 

class autonomous_system:

    def __init__(self, as_id, igp, community, community_number):
        self.as_id = as_id
        self.community = community # "customer", "provider", "settlement-free peer"
        self.community_number = community_number
        self.routers = {} # router_id : router(object)
        self.link_dict = {} #(router_id,interface.name):(router_id,interface.name)
        self.loopback_plan = {} # router_id : loopback
        self.igp = igp # OSPF or RIP
        self.bgp = "BGP"


    def construct_link_dict(self):
        link_dict = {}
        for router_id, router in self.routers.items():
            for interface in router.interfaces.values():
                if interface.connected_router is not None:# None means the loopback0
                    link_dict[(router_id, interface.name)]=(interface.connected_router, interface.connected_interface)
                    #(router_id, interface.name): (interface.connected_router, interface.connected_interface) and its reverse
                    link_dict[(interface.connected_router, interface.connected_interface)]=(router_id, interface.name)
        self.link_dict = link_dict

    def update_link_dict(self, r1, r2): #r1, r2 are strings
        link_dict_copy = self.link_dict.copy()
        for (rt1,int1),(rt2,int2) in link_dict_copy.items():
            if rt1 == r1 and rt2 == r2:
                del self.link_dict[(rt1,int1)]
                del self.link_dict[(rt2,int2)]