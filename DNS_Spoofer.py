#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy
import argparse

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload)
    if scapy_packet.haslayer(scapy.DNSRR):
        scapy.packet.show()

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()