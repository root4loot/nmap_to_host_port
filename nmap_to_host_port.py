#!/usr/bin/env python3

# A simple script for parsing .nmap files to output a list of hostname:port pairs.
# It supports outputting all hostnames or deduplicating by IP address.
#
# Usage:
# To output all hostnames with their open ports:
# ./script_name.py <filename.nmap>
#
# To deduplicate by IP and output the first hostname for each IP with open ports:
# ./script_name.py <filename.nmap> --unique-hosts
#
# Author: Daniel Antonsen @rootloot

import sys
import re
import argparse

def extract_and_process_nmap_reports(filename, unique_hosts=False):
    """
    Extracts sections from an Nmap file that start with 'Nmap scan report for',
    identifies hostname or IP and open ports within those sections,
    and prints a sorted, unique list of 'hostname or IP:port'.
    If unique_hosts is True, only the first hostname for each unique IP is processed.
    """
    with open(filename, 'r') as file:
        content = file.read()
    
    pattern = r'Nmap scan report for (?:([^\s]+) \((.*?)\)|(.*?))\n'
    
    matches = re.findall(pattern, content, re.DOTALL)
    
    host_port_pairs = set()
    ip_hostname_map = {}
    
    for match in matches:
        hostname_or_ip = match[0] if match[0] else (match[1] if match[1] else match[2])
        ip = match[1] or match[2]
        
        # For unique hosts, skip if the IP has already been encountered
        if unique_hosts and ip in ip_hostname_map:
            continue
        ip_hostname_map[ip] = hostname_or_ip
        
        ports_section_search = re.search(r'PORT.*?\n((?:\d+/.*?\n)+)', content[content.find(match[0]):], re.DOTALL)
        if ports_section_search:
            port_lines = ports_section_search.group(1).splitlines()
            for port_line in port_lines:
                port_search = re.search(r'(\d+)/tcp\s+open', port_line)
                if port_search:
                    port = port_search.group(1)
                    host_port_pairs.add(f"{hostname_or_ip}:{port}")
    
    # Sorting and printing the unique host:port pairs
    for host_port in sorted(host_port_pairs):
        print(host_port)

def main():
    parser = argparse.ArgumentParser(description='Extract open port information from Nmap scan reports.')
    parser.add_argument('filename', help='The Nmap scan file to process.')
    parser.add_argument('--unique-hosts', action='store_true',
                        help='Output only the first hostname for each unique IP address.')
    
    args = parser.parse_args()
    
    extract_and_process_nmap_reports(args.filename, args.unique_hosts)

if __name__ == "__main__":
    main()

