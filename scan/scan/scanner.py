import os
import sys
import struct
import socket


class Scanner:
    def __init__(self):
        self.ips = {}

    def _create_ips_from_range(self, start, end):
        start = struct.unpack("!I", socket.inet_aton(start))[0]
        end = struct.unpack("!I", socket.inet_aton(end))[0]
        for ip in xrange(start, end + 1):
            yield socket.inet_ntoa(struct.pack("!I", ip))

    def scan_ranges(self, ranges_dir):
        for country in os.listdir(ranges_dir):
            for line in open(os.path.join(ranges_dir, country), 'r'):
                try:start, end = line.split('-')
                except ValueError:
                    sys.stderr.write("invalid format: %s\n" % line)
                    continue
                for ip in self._create_ips_from_range(start, end):
                    print ip
