class router:
   
    def __init__(self,type="Internal"):
        #self.name = name
        self.router_id = None
        self.loopback = None
        self.loopback_interface = None #interface name
        self.all_interfaces = {} #interface.name : occupied? (1 or 0)
        #self.routing_table = {} ##maybe not needed
        self.interfaces = {} #interface.name: interface(object)
        self.neighbours = [] #router_id, extrait de self.interface
        self.type = type # ABR, ASBR, Internal   

class interface:
    
    def __init__(self,name,protocol_type=None):
        self.name = name
        self.tag = 0 # 1 for loopback
        self.statu = None # up or down
        self.address_ipv6_global = None
        self.netmask = None
        self.connected_router = None # router_id
        self.connected_interface = None # interface.name
        self.protocol_type = protocol_type   
        self.protocol_process = None 

class autonomous_system:

    def __init__(self, as_id, igp):
        self.as_id = as_id
        self.routers = {} # router_id : router(object)
        self.link_lst = [] # (router_id,interface.name,router_id,interface.name)
        self.loopback_plan = {} # router_id : loopback
        self.igp = igp # OSPF or RIP
        self.bgp = "BGP"

    def construct_link_lst(self):
        new_link_lst = []
        for router_id, router in self.routers.items():
            for interface in router.interfaces.values():
                if interface.connected_router is not None:
                    link = ((router_id, interface.name), (interface.connected_router, interface.connected_interface))
                    #eliminate duplicates
                    reverse_link = (link[1], link[0])
                    if link not in new_link_lst and reverse_link not in new_link_lst:
                        new_link_lst.append(link)
        self.link_lst = new_link_lst