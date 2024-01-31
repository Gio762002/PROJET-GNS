# PROJECT-GNS  
by Yizuo GUO, Xinyu ZHAO, Yichao MAO  
## What does this project do:   

Automatically generate router configuration files in .cfg version in the folder ```output``` from a network intent file ```network_intent.json```. the .cfg files could be placed in the right folder at your path of GNS3, and be ran without errors once the topologie was set.    

We have been excepting this project to have some level of automation, rather than blindly transporting the associated commands from the intent file. This is why we designed this 'simulator' program who tries imite human network architect.  

The design of the program bring us another profit is that you can always call functions defined in ```show.py``` at any place in the main program to print out information you want in your terminal. this sort of visualisation might be more clear and direct.

## How does it work?  
There's several python files that achieve the conversion form an intent file to configuration files. The passage of this conversion is:  

**read intent line by line -> build the overrall topologie by simulations -> generate configuration files in order**  

### python files needed :  

**read intent** :  
- ```read_network_intent.py``` : reads from a json file(maybe).  

**overall topologie** :  
- ```class_reseau.py``` : defines classes for router/interface/as.  
- ```fct_reseau.py``` : defines all the fct that are useful to build the topologie ex: add one router to an as.  
- ```fct_protocol_reg.py``` : defines all the fct that relate to implementations of protocols with ```reg``` as a parameter that tracks Cisco commands related.     

**generate outputs**:    
- ```class_output.py``` : defines the ```registrar``` class, that registrer Cisco commands from the right loop, and group the commands by router and interface.   
- ```fct_protocol_reg.py``` :  pass ```reg``` as a parameter, which is a ```registrar``` instance, created in the main program.  

**principal programme** :   
- ```main.py``` : use all instances(defined by classes), clear out the order of call of the functions.    

#### other python files that help with testing:  
- ```fct_show.py```: modular visualization functions.  
- ```test.py```: sample of testing all the functions, can be considered as a simulation. 

### HOW TO RUN IT : Simply run ```main.py``` :)  
##### what you can play in the ```main.py``` :   
- change json file to read by modifying its path
- change the path where you want to store your outputs, but please use always a folder that already exists

###### if you could not run the program, check if all the relying files are imported correctly, if not, try to use ```sys.path.append``` to add to path.