#!/usr/bin/env python 
 
import scapy.all as scapy 
import argparse
def get_ip():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r","--range",dest="ip",help="Type an ip or a range")
    options = parser.parse_args()
    if not options.ip:
        parser.error("[-] Please Specify an ip or a range , use -h for more information ")
    return options
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0]
    Client_List= []
    for element in answered_list:
        Client_dict = {"IP":element[1].psrc , "MAC":element[1].hwsrc}
        Client_List.append(Client_dict)
    
    return Client_List

def print_result(Scan_result):
    print("[+] ---------------------- NETWORK SCANNER By 0xHex  ---------------------- [+]")
    print("IP\t\t\tMAC ADDRESS\n----------------------------------------------------------------")
    for client in Scan_result:
        print(client["IP"]+"\t\t"+client["MAC"])

options = get_ip()
Scan_result = scan(options.ip)
print_result(Scan_result)
