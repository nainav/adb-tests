import os
import re
import time
import subprocess
import pexpect
from avocado import Test
#This method is doing Vagrant up with the specific provider 
def vagrantUp(self, path):
    self.log.debug(" Vagrant up:: Start")
    self.log.debug("changing path to " + path)
    os.chdir(path)
    paramerters = pexpect.spawn("vagrant up --provider "+self.params.get('vagrant_PROVIDER'))
    paramerters.expect('.*Would you like to register the system now.*', timeout=250)
    paramerters.sendline("y")
    paramerters.expect(".*username.*")
    paramerters.sendline(self.params.get('vagrant_RHN_USERNAME'))
    # paramerters.sendline("naverma@redhat.com")
    paramerters.expect(".*password.*")
    paramerters.sendline(self.params.get('vagrant_RHN_PASSWORD'))
    # paramerters.sendline("*****")
    paramerters.interact()
    paramerters.close()
    time.sleep(20)
    out=global_status(self,path)
    self.assertTrue( 'running' in out)
	#self.log.debug(" Vagrant up:: Exit")

    return out

#Returning Global status
def global_status(self, vm_name):
    self.log.debug("Checking Global status ::Start")
    self.log.info("vagrant global-status |grep " + vm_name + " |awk '{print $4}'")
    p = subprocess.Popen("vagrant global-status |grep " + vm_name + " |awk '{print $4}'", stdout=subprocess.PIPE,
                         shell=True)
    (output, err) = p.communicate()
    self.log.debug(output)
	#self.log.debug("Checking Global status ::Exit")
    return output,err


def vagrantDestroy(self,path):
    self.log.info( " vagrant destroy ::Start")
    os.chdir(path)
    p = subprocess.Popen("vagrant destroy --force", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    self.log.debug(output)
    self.log.info('*******************8')
    #self.assertTrue('==> default: Destroying VM and associated drives' in output)
	
    return output,err


def vagrantSSH(self,command):
    self.log.info( "vagrant SSH :: Start" )
    p = subprocess.Popen("vagrant ssh -c "+command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    self.log.debug(output)
	
    return output


def vagrant_service_manager(self, path, command):
    self.log.debug("vagrant_service_manager module inside Utils:: Start")
    self.log.debug("changing path to " + path)
    os.chdir(path)
    p = subprocess.Popen("vagrant service-manager " + command)
    (output, err) = p.communicate()
    self.log.debug(output)
	#self.log.debug("vagrant_service_manager module inside Utils:: Finish")
    return output


def vagrant_box_add(self):
    self.log.info("Vagrant Box add :: Start")
    if os.path.isfile(self.params.get('vagrant_BOX_PATH')) ==True:
        pass
    p = subprocess.Popen('vagrant box add cdkv2 '+ str(self.params.get('vagrant_BOX_PATH')))
    (output, err) = p.communicate()
    self.log.debug(output)
    return output

def vagrant_box_remove(self):
    self.log.info("Vagrant Box Remove :: Start")
    p = subprocess.Popen("vagrant box remove cdkv2 --force")
    (output, err) = p.communicate()
    self.assertTrue('Removing box' in output)
  #  self.log.info("Vagrant Box Remove ::Finish")
    return output

def vagrant_plugin_install(self):
    try:
        self.log.info("Vagrant Plugin Install :: Start")
        os.chdir(self.params.get('vagrant_PLUGINS_DIR'))
        #os.system("vagrant plugin install ./vagrant-registration-*.gem  ./vagrant-service-manager-*.gem ./vagrant-sshfs-*.gem")
        p = subprocess.Popen("vagrant plugin install ./vagrant-registration-*.gem  ./vagrant-service-manager-*.gem ./vagrant-sshfs-*.gem")
        (output, err) = p.communicate()
        self.log.debug(output)
        #return output
    except:
         self.log.info('Exception!')
         #return output
#    self.log.info("Vagrant Plugin Install ::Finish")

    

# This method is for multi windows shell support ,it runs the specific commands in the particalar sheels 
def shell_commands(self, command):
    self.log.info("This method is used because we need to provide support for Powershell , cmd, cygwin, bash,ubuntu")
    if self.params.get('Windows_Shell') == 'powershell':
        operator = '|'
        shell_output = subprocess.Popen([r'C:/WINDOWS/system32/WindowsPowerShell/v1.0/powershell.exe',command],cwd=os.getcwd())
        result = shell_output.wait
        time.sleep(20)
        self.log.debug('Suspend result :' + str(result))
        return shell_output
    elif self.params.get('Windows_Shell') == 'cmd':
        operator = '&'
        shell_output = subprocess.Popen([r'C:/Windows/System32/cmd.exe',command],
                                    cwd=os.getcwd())
        result = shell_output.wait
        time.sleep(20)
        self.log.debug('Suspend result :' + str(result))
        return shell_output
    else:
        os.chdir(self.params.get('vagrant_VARGRANTFILE_DIRS'))
        shell_output = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True,cwd=os.getcwd())
        (output, err) = shell_output.communicate()
        self.log.debug(output)
        return output
