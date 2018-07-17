import sys
import os
from subprocess import Popen, PIPE
import subprocess
from shlex import split


# 1. ethernet setup
#vi /etc/udev/rules.d/70-persistent-ipoib.rules 
def setupEth():
    print( "##### start ethernet setup #####")
    os.system("sudo yum install -y net-tools")
    print("Enter number of port to use in Openstack: ")
    try:
        num = raw_input()
    except SyntaxError:
        num = None
    if num is None:
        print("Error->" + num )
        exit(1);
    i = 0
    while i < int(num):
        print("Enter " +str(i+1)+ " ethernet device name:")
        try:
            origDev = raw_input()
        except SyntaxError:
            origDev = None
        if origDev is None:
            print("Error" + origDev )
            exit(1);

        print("Enter "+str(i+1)+"ethernet device name to be changed:")
        try:
            chgDev = raw_input()
        except SyntaxError:
            chgDev = None
        if chgDev is None:
            print("Error" + chgDev )
            exit(1);

        p1 = Popen( split("ifconfig "+ origDev ), stdout=PIPE)
        p2 = Popen( split("grep ether"), stdin=p1.stdout, stdout=PIPE)
        output = p2.stdout.read()
        mac = split(output)[1]
        print( origDev + " find mac->" + mac )

        eth = "ACTION==\"add\", SUBSYSTEM==\"net\", DRIVERS==\"?*\", ATTR{type}==\"1\" ATTR{address}==\""
        eth = eth + mac + "\" NAME=\""+chgDev+"\""

        subprocess.call("echo '"+eth+"' >> /etc/udev/rules.d/70-persistent-ipoib.rules", shell=True)

        path = "/etc/sysconfig/network-scripts"
        org = path+"/ifcfg-"+origDev
        dst = path+"/ifcfg-"+chgDev

        with open( org, "r" ) as fRead:
            with open( dst, "w" ) as fWrite:
                for line in fRead:
                    print( line )
                    fWrite.write( line.replace( origDev, chgDev) )
        os.system("sudo mv "+org+ " " + org+".bk" );
        i = i + 1

# 2. character set 
# vi /etc/environment
#LANG=en_US.utf-8 
#LC_ALL=en_US.utf-8
def setupCharSet() :
    print( "##### utf8 character set #####")
    subprocess.call("sudo echo LANG=en_US.utf-8 >> /etc/environment", shell=True)
    subprocess.call("sudo echo LC_ALL=en_US.utf-8 >> /etc/environment", shell=True)

# 3. service stop
# systemctl stop postfix firewalld NetworkManager 
# systemctl disable postfix firewalld NetworkManager 
def setupService() :
    print( "##### setup service #####")
    subprocess.call("sudo systemctl stop postfix firewalld NetworkManager", shell=True)
    subprocess.call("sudo systemctl disable postfix firewalld NetworkManager", shell=True)

# 4. selinux
# setenforce 0 
# getenforce 
# vi /etc/selinux/config
#SELINUX=disabled
def setupSelinux():
    print( "##### disable selinux #####")
    os.system("sudo setenforce 0")
    subprocess.call("sudo echo SELINUX=disabled > /etc/selinux/config", shell=True)

def installOpenstack():
    print("What type of node? : ")
    print("1. controller")
    print("2. compute")
    try:
        type = raw_input()
    except SyntaxError:
        type = None
    if type is None:
        print("Error->" + type )
        exit(1);

    if int(type) == 1:
        print( "##### install openstack #####")
        os.system("sudo yum search centos-release-openstack" )
        print("Enter openstack release: ")
        try:
            rel = raw_input()
        except SyntaxError:
            rel = None
        if rel is None:
            print("Error->" + rel )
            exit(1);
        os.system("sudo yum install -y " + rel)
        os.system("sudo yum update -y")
        os.system("sudo yum install -y openstack-packstack")
        os.system("sudo yum install -y openstack-utils")
    else:
        os.system("sudo yum update -y")

#main
print("###############################")
print("# Setup Openstack Environment #")
print("###############################")
setupEth()
setupCharSet()
setupSelinux()
setupService()
installOpenstack()

print("##################################################")
print("##################################################")
print("##### OPENSTACK ENVIRONMENT SETUP FINISH!!!! #####")
print("##################################################")
print("##### Please reboot system!")
print("##################################################")

#os.system("sudo reboot")


