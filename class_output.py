import os
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
    
    def display(self, root, indent=0): 
        for key, value in root.items(): 
            print('\t' * indent + '--' + str(key))
            if isinstance(value, dict):
                self.display(value, indent+1)
            elif isinstance(value, list):
                for i in value:
                    print('\t' * (indent+1) + '--' + str(i))
            else:
                print('\t' * (indent+1) + '--' + str(value))

    def save_as_txt(self):
        files = {}
        for target in self.general_register.keys():
            files[target] = "output/" + target + ".txt"
        
        for (target, file) in files.items():
            if os.path.exists(file):  # Check if the file exists
                os.remove(file)  # Delete the file
            
            with open(file, "w") as f:
                for key, value in self.general_register[target].items():
                    if key == "general":
                        for i in value:
                            f.write(i + "\n")
                    else:
                        f.write(key + "\n")
                        for i in value:
                            f.write("\t" + i + "\n")
