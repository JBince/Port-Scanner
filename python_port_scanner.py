#!/usr/bin/python3
import socket
import sys
from datetime import datetime
import argparse
from target import Target

# Arguments
parser = argparse.ArgumentParser(description='A simple Python3 port scanner')
req_args = parser.add_argument_group('Required named args')
req_args.add_argument('-t', '--target', help='Target IP Address')
req_args.add_argument(
    '-p', '--ports', help='Port specification. Should be a range (x-y), a single port (x), or "all" for a full 65,535 port scan')
parser.add_argument('-b','--banner',help='Grab banners from ports',action='store_true')
args = parser.parse_args()

open_ports = []
def scan():
    t1 = Target(args.target,args.ports)
    scan_type = t1.determine_type()
    try:
        target = socket.gethostbyname(args.target)
        # Establish if the selection is all, a single port, or a range of ports
        #For all ports
        if scan_type == 'all':
            for p in range(1, 65535):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                # Test port
                result = sock.connect_ex((target, p))
                if result == 0:
                    print(f'{p} is Open')
                    open_ports.append(p)
                sock.close()

        #For a single port
        elif scan_type == 'single_port':
            port = int(args.ports)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            # Test port
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f'{args.ports} is open')
                open_ports.append(args.ports)
            else:
                print(f'{port} is closed')
            sock.close()

        #For a port range
        elif scan_type == 'port_range':
            start = int(args.ports.split('-')[0])
            end = int(args.ports.split('-')[1])
            for p in range(start, end):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                # Test range
                result = sock.connect_ex((target, p))
                if result == 0:
                    print(f'{p} is open')
                    open_ports.append(p)
        else:
            print('[*] Invalid Port Selection')
            exit()
    finally:
        pass

def grab_banner():
    for p in open_ports:
        try:
            s= socket.socket()
            s.connect((args.target,int(p)))
            banner = s.recv(1024).decode('utf-8')
            print(f'Port {p}: {banner}')
            s.close()
        except:
            print(f'Could not get banner for port {p}')

def main():
    try:
        print(args.ports)
        scan()
        grab_banner()
    except KeyboardInterrupt:
        print('\n[*] Exiting')
        sys.exit()
    except socket.gaierror:
        print("\n[*] Could not resolve host")
        sys.exit()
    except socket.error:
        print("\n[*] Server not responding")
        sys.exit()

main()