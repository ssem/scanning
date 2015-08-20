import sys
import struct
import socket
import select


class Send:
    def __init__(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            self.s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        except socket.error:
            sys.exit("Socket could not be created")

    def _create_ip_header(self, source_ip, dest_ip,
            ihl=5, version=4, tos=0, tot_len=40, id=54321, frag_off=0, ttl=255,
            protocol=socket.IPPROTO_TCP, check=10):

        saddr = socket.inet_aton(source_ip)
        daddr = socket.inet_aton(dest_ip)
        ihl_version = (version << 4) + ihl
        return struct.pack('!BBHHHBBH4s4s', ihl_version, tos, tot_len, id, frag_off,
                                            ttl, protocol, check, saddr, daddr)

    def _create_tcp_header(self, source_ip, dest_ip, source_port, dest_port,
            seq=0, ack_seq=0, doff=5, fin=0,syn=1, rst=0, psh=0, ack=0,
            urg=0, window=5840, protocol=socket.IPPROTO_TCP, check=0, urg_ptr=0):

        window = socket.htons(window)
        offset_res=(doff << 4) + 0
        tcp_flags = fin + (syn << 1) + (rst << 2) + (psh <<3) + (ack << 4) + (urg << 5)
        tcp_header = struct.pack('!HHLLBBHHH', source_port, dest_port, seq, ack_seq,
                                               offset_res, tcp_flags, window, check, urg_ptr)
        source_address = socket.inet_aton(source_ip)
        dest_address = socket.inet_aton(dest_ip)
        tcp_length = len(tcp_header)
        psh = struct.pack('!4s4sBBH' ,source_address, dest_address, 0, protocol, tcp_length);
        psh += tcp_header;
        s = 0
        for i in range(0, len(psh), 2):
            w = (ord(psh[i]) << 8) + (ord(psh[i+1]) )
            s = s + w
        s = (s>>16) + (s & 0xffff);
        check = ~s & 0xffff
        return struct.pack('!HHLLBBHHH', source_port, dest_port, seq, ack_seq, offset_res,
                                         tcp_flags, window, check, urg_ptr)

    def send_syn_packet(self, source_ip, dest_ip, source_port, dest_port):
        ip_header = self._create_ip_header(source_ip, dest_ip)
        tcp_header = self._create_tcp_header(source_ip, dest_ip, source_port, dest_port)
        try:self.s.sendto(ip_header + tcp_header, (dest_ip, 0))
        except:pass


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

    def yield_all(self):
        while True:
            try:
                inp, outp, execption = select.select([self.s], [], [])
                for sock in inp:
                    packet, source = sock.recvfrom(4096)
                    packet = self._unpack_tcp_header(packet)
                    yield source[0], packet['source port']
            except:pass

    def yield_synack(self):
        while True:
            try:
                inp, outp, execption = select.select([self.s], [], [])
                for sock in inp:
                    packet, source = sock.recvfrom(4096)
                    tcp = self._unpack_tcp_header(packet)
                    if tcp['flags'] == 18 and tcp["dest port"] == 58124:
                        yield source[0], tcp["source port"]
            except:pass
