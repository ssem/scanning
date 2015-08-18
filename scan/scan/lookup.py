import os
import sys
import struct
import socket


class Node:
    def __init__(self, lower, upper, country):
        self.lower = lower
        self.upper = upper
        self.country = country
        self._left = None
        self._right = None

class Lookup:
    def __init__(self):
        self.binary_tree = None

    def _add(self, node):
        if self.binary_tree is None:
            self.binary_tree = node
        else:
            self._recursive_add(node, self.binary_tree)

    def _recursive_add(self, node, curser):
        if node.lower < curser.lower:
            if curser._left != None:
                self._recursive_add(node, curser._left)
            else:
                curser._left = node
        else:
            if curser._right != None:
                self._recursive_add(node, curser._right)
            else:
                curser._right = node

    def add_range_dir(self, range_dir):
        for f in os.listdir(range_dir):
            self.add_range_file(os.path.join(range_dir, f))

    def add_range_file(self, range_file):
        f = open(range_file, 'r')
        for line in f:
            try:
                if not line.startswith("#"):
                    ip1, ip2 = line.split('-')
                    lower = int(struct.unpack('!I', socket.inet_aton(ip1))[0])
                    upper = int(struct.unpack('!I', socket.inet_aton(ip2))[0])
                    self._add(Node(lower, upper, os.path.basename(range_file)))
            except ValueError: sys.stderr.write('\033[91m[-]\033[1;m RangeError invalid format: %s\n' % line)
            except socket.error: sys.stderr.write('\033[91m[-]\033[1;m RangeError invalid ip address: %s\n' % line)
        sys.stdout.write('\033[92m[+]\033[1;m Loaded: %s\n' % os.path.basename(range_file))

    def _recursive_find(self, ip, curser):
        if ip < curser.lower and curser._left != None:
            return self._recursive_find(ip, curser._left)
        elif ip >= curser.lower:
            if ip <= curser.upper:
                return curser
            elif curser._right != None:
                return self._recursive_find(ip, curser._right)

    def find(self, ip):
        ip = int(struct.unpack('!I', socket.inet_aton(ip))[0])
        if self.binary_tree is not None:
            try:return self._recursive_find(ip, self.binary_tree).country
            except:return 'unknown'
