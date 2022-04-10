#!/usr/bin/python3
import socket
import sys
from datetime import datetime
import argparse
import pyfiglet

# Arguments
parser = argparse.ArgumentParser(description='A simple Python3 port scanner')
req_args = parser.add_argument_group('Required named args')
req_args.add_argument('-t', '--target', help='Target IP Address')
req_args.add_argument(
    '-p', '--ports', help='Port specification. Should be a range (x-y), a single port (x), or "all" for a full 65,535 port scan')
args = parser.parse_args()

try:
    target = socket.gethostbyname(args.target)
    # Establish if the selection is all, a single port, or a range of ports
    #For all ports
    if args.ports == 'all':
        for p in range(1, 65535):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            # Test port
            result = sock.connect_ex((target, p))
            if result == 0:
                print(f'{p} is Open')
            sock.close()
    #For a single port
    elif args.ports.find('-') != 1:
        port = int(args.ports)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        # Test port
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f'{args.ports} is open')
        else:
            print(f'{port} is closed')
        sock.close()
    #For a port range
    elif args.ports.find('-') == 1:
        start = int(args.ports.split('-')[0])
        end = int(args.ports.split('-')[1])
        for p in range(start, end):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            # Test range
            result = sock.connect_ex((target, p))
            if result == 0:
                print(f'{p} is open')
    else:
        print('[*] Port selection invalid')


except KeyboardInterrupt:
    print('\n[*] Exiting')
    sys.exit()
except socket.gaierror:
    print("\n[*] Could not resolve host")
    sys.exit()
except socket.error:
    print("\n[*] Server not responding")
    sys.exit()