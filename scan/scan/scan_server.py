import os
import sys
import time
import struct
import socket
import random
import argparse
import multiprocessing
from scan.raw_sock import Send

class Scan_Server:
    def __init__(self):
        self.my_ip = self._get_my_ip()
        self._send = Send()
        self._attempts_q = multiprocessing.Queue()
        self._attempts = 0
        self.total = 0

    @property
    def attempts(self):
        while not self._attempts_q.empty():
            self._attempts += self._attempts_q.get()
        return self._attempts

    def _get_my_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com", 80))
        my_ip = s.getsockname()[0]
        s.close()
        return my_ip

    def _randomizer(self, ranges):
        jump = 437
        for offset in reversed(xrange(jump)):
            for rang in ranges:
                count = 0
                done = False
                while not done:
                    ip = rang['start'] + (count * jump + offset)
                    if ip <= rang['end']:
                        try:yield socket.inet_ntoa(struct.pack('!L', ip))
                        except:pass
                    else:
                        done = True
                    count += 1

    def _get_ranges(self, ranges_dir):
        total = 0
        ranges = []
        if not os.path.isdir(ranges_dir):
            exit("Range_dir options is not a Directory")
        for country in os.listdir(ranges_dir):
            for line in open(os.path.join(ranges_dir, country), 'r'):
                if not line.startswith("#"):
                    try:
                        start, end = line.split('-')
                        start = struct.unpack("!L", socket.inet_aton(start))[0]
                        end = struct.unpack("!L", socket.inet_aton(end))[0]
                        total += end - start + 1
                        ranges.append({"start":start, "end":end, "country":country})
                    except ValueError:
                        sys.stderr.write("invalid range: %s\n" % line.rstrip("\n"))
                    except Exception as e:
                        sys.stderr.write(str(e))
        return ranges, total

    def _get_ports(self, ports_file):
        ports = []
        if not os.path.isfile(ports_file):
            exit("Ports_file options is not a File")
        for line in open(ports_file, 'r'):
            if not line.startswith("#"):
                try:
                    port = line.rstrip("\r\n").split(" ")[0]
                    if len(port) > 0:
                        ports.append(int(port))
                except Exception as e:
                    sys.stderr.write(str(e))
        return ports

    def _scan(self, ranges_dir, ports_file, rate, queue):
        start = time.time()
        rate = int(rate) * 2
        attempts = 0
        ranges, total = self._get_ranges(ranges_dir)
        ports = self._get_ports(ports_file)
        queue.put(total * len(ports))
        for port in ports:
            for ip in self._randomizer(ranges):
                try:
                    self._send.send_syn_packet(self.my_ip, ip, 58124, port)
                    attempts += 1
                    queue.put(1)
                    if attempts % rate == 0:
                        try:time.sleep(2 - (time.time() - start))
                        except:pass
                        start = time.time()
                except:pass

    def scan(self, ranges_dir, ports_file, rate):
        self.scan_server = multiprocessing.Process(
            target=self._scan,
            args=(ranges_dir, ports_file, rate, self._attempts_q))
        self.scan_server.daemon = True
        self.scan_server.start()
        self.total = self._attempts_q.get()
        print "\033[92m[+]\033[1;m Scanning"

    def wait(self, timeout=None):
        self.scan_server.join(timeout)

    def is_alive(self):
        return self.scan_server.is_alive()

    def __del__(self):
        try:self.scan_server.terminate()
        except:pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("range_dir", help="range directory")
    parser.add_argument("port_file", help="port file")
    parser.add_argument("rate", help="scan rate")
    args = parser.parse_args()
    ss = Scan_Server()
    ss.scan(args.range_dir, args.port_file, args.rate)
    ss.wait()
