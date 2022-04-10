#!/usr/bin/python3

class Target():
    def __init__(self, host, ports):
        self.host = host
        self.ports = ports

    def determine_type(self):
        #For a full scan
        if self.ports == 'all':
            return 'all'

        #Single Port
        elif self.ports.find('-') != 1:
            port = int(self.ports)
            return 'single_port'

        #Port Range
        elif self.ports.find('-') == 1:
            return 'port_range'
