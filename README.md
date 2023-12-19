# PROJET-GNS  

## Basic thoughts for how we are going to do  

There's several python files that achieve the conversion form an intent file to Cisco command file. The passage of this conversion will be:  

**read intent -> have the overview of the topologie -> generate Cisco commands by order**  

### python files needed :  

**read intent** : ```read.py``` read from a json file(maybe).  

**topologie overview** : ```class.py``` : define classes for router/as/protocol.  ```configure.py```: define all the fct that are usefull to build the topologie ex: add one router to an as.  

**generate commands**: ```commands.py```: contains all the commands that need to be sorted by order.  

**principal programme** : ```main.py``` : use all objets(defined by classes), clear out the order of commands.  

**the point that might be the most difficult: sort the order of commands**   
