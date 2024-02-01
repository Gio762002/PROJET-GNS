import os
class registrar(): 
    '''
    designed for routers and their interfaces, generate output files
    '''
    def __init__(self,path="output/"):
        self.general_register = {}
        self.log = {}
        self.path = path
    def create_register(self, name):
        self.general_register[name] = {0:[],
                                       1:{"a":[],"b":[],"c":[],"c":[],"d":[],"e":[],"f":[],"g":[],"h":[],"i":[],"j":[],"k":[],"l":[]},
                                       2:[],
                                       3:[],
                                       4:{"in":[],"out":[]},
                                       5:[],
                                       "Loopback0":[]} 
        self.log[name] = {}
        """
        writing order:
        # 0 : default
        # 1 : bgp (but specific inside by caracters)
        # 2 : ospf/rip
        # 3 : prefix-list
        # 4 : route-map
        """
    
    def add_entry(self, name, entry): #put interface.name or writing order here as entry
        self.general_register[name][entry] = []
        self.log[name][entry] = { "route_map_name": None}

    def write(self, name, entry, command,second=None):
        try:
            if name in self.general_register and entry in self.general_register[name]:
                if second != None:
                    self.general_register[name][entry][second].append(command)
                else:
                    self.general_register[name][entry].append(command)
            else:
                print("Invalid name or entry")
        except Exception as e:
            print("Error:", str(e))

    def save_as_cfg(self):
        files = {}
        for target in self.general_register.keys():
            files[target] = self.path +"i" + target[1:] + "_startup-config.cfg"
        
        for file_name in os.listdir(self.path):
            if file_name.endswith(".cfg"):
                file_path = os.path.join(self.path, file_name)
                os.remove(file_path)
                
        for (target, file) in files.items():         
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
                        if isinstance(value, dict):#designed for bgp
                            for second in value.values():
                                for i in second:
                                    f.write(i + "\n")
                        else:
                            for i in value:
                                f.write( i + "\n")
                        
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
            "!",
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
            # "gatekeeper",
            # " shutdown",
            # "!","!",
            # "line con 0",
            # " exec-timeout 0 0",
            # " privilege level 15",
            # " logging synchronous",
            # " stopbits 1",
            # "line vty 0 4",
            # " login",
            # "!","!",
            # "end"
        ] # commented to ensure telnet.py works
        if where == "beginning":
            for command in default_commands_beginning:
                f.write(command+"\n")
        elif where == "end":
            for command in default_commands_end:
                f.write(command+"\n")

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

