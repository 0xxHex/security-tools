#!/usr/bin/env python 

import argparse
import subprocess
import re

def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--interface",dest="interface",help="Interface for change it's MAC Address")
    parser.add_argument("-m","--new_mac",dest="new_mac",help="MAC Address for change the oldest One")
    options = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please Specify an inteface , use -h for information ")
    
    if not options.new_mac:
        parser.error("[-] Please Specify a NEW MAC , use -h for information ")
    
    return options

def change_mac(interface,new_mac):
    print("[+] ---------------------- MAC CHANGER By 0xHex  ---------------------- [+]")
    print(f"[+] Changing MAC Address for {interface} to {new_mac} [+]")
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface,"hw","ether",new_mac])
    subprocess.call(["ifconfig",interface,"up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig",interface])
    mac_address_searching_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(ifconfig_result))
    if mac_address_searching_result:
        return mac_address_searching_result.group(0)
    else : 
        print("[-] Could not read MAC Address from your input interface [-]")



options = get_argument()
current_mac = get_current_mac(options.interface)
print(f"Your Current MAC is : {current_mac}")
change_mac(options.interface,options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] Your MAC Address has been changed successfully :) [-]")
else : 
    print("[-] Could not change MAC Address for this interface please try again :( [-]") 
