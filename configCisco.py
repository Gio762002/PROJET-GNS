import class_reseau as classr
import fct_reseau as fctr
import fct_protocol as fctp


'''need write Cisco command to output (commands associated)'''
def config_unused_interface(router):
    for int_name, status in router.all_interfaces.items():
        if status == 0:
            interface = router.interfaces[int_name].name
            pass 
            #print("interface " + interface)
            #print("no ipv6 address")
            #print("shutdown")
            #print("negotiation auto")
            #print("!")
            
