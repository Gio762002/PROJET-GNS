import class_reseau as classr
import fct_reseau as fctr
import fct_protocol as fctp

def config_unused_interface(router):
    for interface, status in router.all_interfaces.items():
        if status == 0:
            pass #need write Cisco command to output
            #print("interface " + interface)
            #print("no ipv6 address")
            #print("shutdown")
            #print("negotiation auto")
            #print("!")
            
