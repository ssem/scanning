import sys
import struct
import socket


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
        self.s.sendto(ip_header + tcp_header, (dest_ip, 0))


if __name__ == "__main__":
    s = Send()
    import netaddr
    #for ip in netaddr.iter_iprange("60.246.0.0", "60.246.255.255"):
    #    s.send_syn_packet("172.16.5.118", ip, 58124, 80)
    s.send_syn_packet("172.16.5.118", "63.88.73.122", 58124, 80)
