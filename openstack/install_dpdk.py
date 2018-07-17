import sys
import os
from subprocess import Popen, PIPE
import subprocess
from shlex import split


# 1. install develop library
#vi /etc/udev/rules.d/70-persistent-ipoib.rules 
def installLibrary():
    print( "##### install dev tools #####")
    os.system("sudo yum -y groupinstall \"Development Tools\"")

    print( "##### install libpcap #####")
    os.system("sudo yum -y install libpcap-devel")

    print( "##### update #####")
    os.system("sudo yum -y update")


#main
print("###############################")
print("# Setup DPDK #")
print("###############################")
installLibrary()


