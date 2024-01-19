# PROJEcT-GNS  

## What does this project do:   

Automatically generate router configuration files in txt version in the folder ```output``` from a network intent file ```network_intent.json```.     

## How does it work?  
There's several python files that achieve the conversion form an intent file to configuration files. The passage of this conversion is:  

**read intent line by line -> build the overrall topologie by simulations -> generate configuration files in order**  

### python files needed :  

**read intent** :  
```read_network_intent.py``` reads from a json file(maybe).  

**overall topologie** :  
```class_reseau.py``` : defines classes for router/interface/as.  
```fct_reseau.py```: defines all the fct that are usefull to build the topologie ex: add one router to an as.  
```fct_protocol_reg.py```:    

**generate outputs**:    
```class_output.py```: defines the ```registrar``` class, that registrer Cisco commands from the right loop, and group the commands by router and interface.   
```fct_protocol_reg```:  use ```reg``` as parametre 

**principal programme** : ```main.py``` : use all objects(defined by classes), clear out the order of commands.    

#### other python files that help with testing:  
```fct_show.py```  modular visualization functions.  
```test.py```  
