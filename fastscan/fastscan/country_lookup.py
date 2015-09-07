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

class Country_Lookup:
    def __init__(self):
        self.binary_tree = None

    def balance_node(self, node):
        if node._right == None and node._left:
            if node._left._right == None and node._left._left:
                new_node = Node(node.lower, node.upper, node.country)
                node.lower = node._left.lower
                node.upper = node._left.upper
                node.country = node._left.country
                node._left = node._left._left
                node._right = new_node
            elif node._left._left == None and node._left._right:
                new_node = Node(node.lower, node.upper, node.country)
                node.lower = node._left._right.lower
                node.upper = node._left._right.upper
                node.country = node._left._right.country
                node._right = new_node
        elif node._left == None and node._right:
            if node._right._right == None and node._right._left:
                new_node = Node(node.lower, node.upper, node.country)
                node.lower = node._right._left.lower
                node.upper = node._right._left.upper
                node.country = node._right._left.country
                node._left = new_node
            elif node._right._left == None and node._right._right:
                new_node = Node(node.lower, node.upper, node.country)
                node.lower = node._right.lower
                node.upper = node._right.upper
                node.country = node._right.country
                node._right = node._right._right
                node._left = new_node

    def _recursive_balance_tree(self, node):
        if node is not None:
            self.balance_node(node)
            self._recursive_balance_tree(node._left)
            self._recursive_balance_tree(node._right)

    def balance_tree(self):
        if self.binary_tree is not None:
            self._recursive_balance_tree(self.binary_tree)

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

    def add(self, node):
        if self.binary_tree is None:
            self.binary_tree = node
        else:
            self._recursive_add(node, self.binary_tree)
            self.balance_tree()

    def add_range_file(self, range_file):
        f = open(range_file, 'r')
        for line in f:
            try:
                if not line.startswith("#"):
                    ip1, ip2 = line.split('-')
                    lower = int(struct.unpack('!I', socket.inet_aton(ip1))[0])
                    upper = int(struct.unpack('!I', socket.inet_aton(ip2))[0])
                    self.add(Node(lower, upper, os.path.basename(range_file)))
            except ValueError: sys.stderr.write('\033[91m[-]\033[1;m RangeError invalid format: %s\n' % line)
            except socket.error: sys.stderr.write('\033[91m[-]\033[1;m RangeError invalid ip address: %s\n' % line)
        sys.stdout.write('\033[92m[+]\033[1;m Loaded: %s\n' % os.path.basename(range_file))

    def add_range_dir(self, range_dir):
        for f in os.listdir(range_dir):
            self.add_range_file(os.path.join(range_dir, f))

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

    def _recursive_print_tree(self, node, depth=0):
        if node is not None:
            new_depth = depth + 1
            print "(%s:%s) %s" % (node.lower, node.upper, new_depth)
            self._recursive_print_tree(node._left, new_depth)
            self._recursive_print_tree(node._right, new_depth)

    def print_tree(self):
        if(self.binary_tree != None):
            self._recursive_print_tree(self.binary_tree)
