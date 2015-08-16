import os
import sys
import socket


class Scanner:
    def __init__(self):
        self.ips = {}

    def _create_ips_from_range(self, start, end):
        start = int(socket.inet_aton(start).encode('hex'),16)
        end = int(socket.inet_aton(end).encode('hex'),16)
        for ip in xrange(start, end):
            print socket.inet_ntoa(ip)

    def scan_ranges(self, ranges_dir):
        for country in os.listdir(ranges_dir):
            for line in open(os.path.join(ranges_dir, country), 'r'):
                try:start, end = line.split('-')
                except ValueError:
                    sys.stderr.write("invalid format: %s\n" % line)
                    continue
                self._create_ips_from_range(start, end)
