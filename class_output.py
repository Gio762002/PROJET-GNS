class registrar(): #designed for routers and their interfaces

    def __init__(self):
        self.general_register = {}

    def create_register(self, name):
        self.general_register[name] = {"general": []} #general: write commun Cisco commands for all interfaces
    
    def add_entry(self, name, entry): #put interface.name here as entry
        self.general_register[name][entry] = []

    def write(self, name, entry, command):
        try:
            if name in self.general_register and entry in self.general_register[name]:
                self.general_register[name][entry].append(command)
            else:
                print("Invalid name or entry")
        except Exception as e:
            print("Error:", str(e))
    
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


