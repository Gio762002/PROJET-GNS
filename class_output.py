class registrar(): #designed for routers and their interfaces

    def __init__(self):
        self.general_register = {}

    def create_register(self, name):
        self.general_register[name] = {"all": []} #all: write commun Cisco commands for all interfaces
    
    def add_entry(self, name, entry):
        self.general_register[name][entry] = []

    def write(self, name, entry, command):
        self.general_register[name][entry].append(command)
    
    def display(self, root, indent=0): # Added missing parameter name
        for key, value in root.items(): # Fixed reference to general_register
            print('\t' * indent + '--' + str(key))
            if isinstance(value, dict):
                self.display(value, indent+1) # Fixed method reference
            elif isinstance(value, list):
                for i in value:
                    print('\t' * (indent+1) + '--' + str(i))
            else:
                print('\t' * (indent+1) + '--' + str(value)) # Fixed reference to indent


'''
quick test, verified
'''
# r = registrar()
# r.create_register("r1")
# r.add_entry("r1", "eth0")
# r.add_entry("r1", "eth1")
# r.write("r1", "eth0", "ipv6 address 2001:100::1/64")
# r.display(r.general_register)