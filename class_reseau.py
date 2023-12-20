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
    
    def __init__(self,name):
        self.name = name
        self.statu = None # up or down
        self.address_ipv6_global = None
        self.connected_router = None
        self.connected_interface = None    

class anonymous_system:

    def __init__(self, as_id, igp):
        self.as_id = as_id
        self.routers = {} # router_id : router(object)
        self.graph = {}
        self.igp = igp # OSPF or RIP
        self.bgp = "BGP"
