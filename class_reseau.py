class router:
   
    def __init__(self,type):
        self.router_id = None
        self.loopback = None
        self.all_interfaces = {} #interface.name : occupied? (1 or 0)
        #self.routing_table = {} ##maybe not needed
        self.interfaces = {} #interface.name: interface(object)
        self.neighbours = [] #router_id, extrait de self.interface
        self.type = type # ABR, ASBR, Internal   

class interface:
    
    def __init__(self,name,protocol_type=None):
        self.name = name
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
        self.loopback_plan = {} # router_id : loopback
        self.igp = igp # OSPF or RIP
        self.bgp = "BGP"
