#!/usr/bin/env python
import sys
import socket
import struct
import select
import binascii

class Receive:
    def __init__(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except socket.error:
            sys.exit("Socket could not be created")

    def _unpack_ip_header(self, packet):
        header = struct.unpack('!BBHHHBBH4s4s', packet[0:20])
        return {"dsf": header[1],
                "total length": header[2],
                "id": header[3],
                "flags": header[4],
                "time to live": header[5],
                "protocol": header[6],
                "checksum": header[7],
                "source ip": socket.inet_ntoa(header[8]),
                "dest ip": socket.inet_ntoa(header[9])}

    def _unpack_tcp_header(self, packet):
        header = struct.unpack('!HHLLBBHHH', packet[20:40])
        return {"source port": header[0],
                "dest port": header[1],
                "seq": header[2], #maybe
                "ack number": header[3],
                "header length": header[4],
                "flags": header[5],
                "window": header[6],
                "checksum": header[7],
                "urg pnt": header[8]}

    def yield_all_ips(self):
        while True:
            return self.s.recvfrom(65565)[1][0]

    def yield_synack_ips(self):
        while True:
            packet, source = self.s.recvfrom(65565)
            if self._unpack_tcp_header(packet)["flags"] == 18:
                print source[0]

if __name__ == "__main__":
        receive = Receive()
        receive.yield_synack_ips()
