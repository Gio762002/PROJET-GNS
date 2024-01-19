import os
class registrar(): #designed for routers and their interfaces

    def __init__(self):
        self.general_register = {}
        self.log = {}

    def create_register(self, name):
        self.general_register[name] = {0:[],1:[],2:[],3:[],4:[],5:[],"Loopback0":[]} 
        self.log[name] = {}
        """
        writing order:
        # 0 : default
        # 1 : bgp
        # 2 : community-list
        # 3 : ospf/rip
        # 4 : prefix-list
        # 5 : route-map
        """
    
    def add_entry(self, name, entry): #put interface.name or writing order here as entry
        self.general_register[name][entry] = []
        self.log[name][entry] = { "route_map_name": None}

    def write(self, name, entry, command):
        try:
            if name in self.general_register and entry in self.general_register[name]:
                if type(entry)!=int:
                    self.general_register[name][entry].append(command)
                else:
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
            files[target] = "output/i" + target[1:] + "_startup-config.cfg"
        
        for (target, file) in files.items():
            if os.path.exists(file): 
                os.remove(file)
            
            with open(file, "w") as f:
                self.write_default(f,target,"beginning")
                for key, value in self.general_register[target].items():
                    if type(key) != int : 
                        f.write("interface "+ key + "\n")
                        for i in value:
                            f.write(" " + i + "\n")
                        f.write("!\n")
                for key, value in self.general_register[target].items():
                    if type(key) == int :
                        for i in value:
                            f.write( i + "\n")
                        # f.write("!\n")
                self.write_default(f,target,"end")
        print("files generated successfully at output/")


    def write_default(self,f,name,where):
        default_commands_beginning=[
            "!", " ", "!",
            "upgrade fpd auto",
            "version 12.4",
            "service timestamps debug datetime msec",
            "service timestamps log datetime msec",
            "no service password-encryption",
            "!",
            f"hostname {name}",
            "!",
            "boot-start-marker",
            "boot-end-marker",
            "!",
            "!",
            "no aaa new-model",
            "no ip icmp rate-limit unreachable",
            "ip cef",
            "!","!","!","!",
            "no ip domain lookup",
            "ipv6 unicast-routing",
            "multilink bundle-name authenticated",
            "!","!","!","!","!","!","!","!","!","!","!","!","!","!",
            "archive",
            " log config",
            "  hidekeys",
            "!","!","!","!",
            "ip tcp synwait-time 5",
            "!","!","!","!",
        ]

        default_commands_end=[
            "!","!","!","!","!","!","!",
            "control-plane",
            "!","!","!","!","!","!","!",
            "gatekeeper",
            " shutdown",
            "!","!",
            "line con 0",
            " exec-timeout 0 0",
            " privilege level 15",
            " logging synchronous",
            " stopbits 1",
            "line vty 0 4",
            " login",
            "!","!",
            "end"
        ]
        if where == "beginning":
            for command in default_commands_beginning:
                f.write(command+"\n")
        elif where == "end":
            for command in default_commands_end:
                f.write(command+"\n")


