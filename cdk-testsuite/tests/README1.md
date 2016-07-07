Purpose cmd.py
--------------
File cmd.py contains the test cases for different windows shell for example (Powershell ,cmd, cygwin)

How to use :
------------
* Add parameter, 
      Windows_Shell : 'powershell' in config.yaml .
      
* def sh_cmd(self,command,shell='powershell') , this method should be used.
* Run command :
      avocado run cmd.py --multiplex ../config/config.yaml
