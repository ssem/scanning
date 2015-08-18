import os
import sys
import json
import time
import socket
import inspect
try:import netaddr
except:exit("Missing netaddr\nTry: sudo pip install netaddr\n")
import multiprocessing
from scan import banners
from scan.send import Send
from scan.receive import Receive
from scan.lookup import Lookup

class Scanner:
    def __init__(self):
        self._send = Send()
        self._receive = Receive()
        self._lookup = Lookup()
        self._banner_modules = self._load_banner_modules()
        self._found_queue = multiprocessing.Queue()
        self.my_ip = self._get_my_ip()
        self.listen_server = None
        self.results_collector = None
        self.found = 0
        self.attempts = 0

    def _get_my_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com", 80))
        my_ip = s.getsockname()[0]
        s.close()
        return my_ip

    def _load_banner_modules(self):
        banner_modules = {}
        classmembers = inspect.getmembers(banners, inspect.isclass)
        for classmember in classmembers:
            if classmember[0] != "Parent" and classmember[0] != "Process":
                cm = classmember[1]()
                banner_modules[int(cm.default_port)] = cm
        return banner_modules

    def _iterate_ips_and_country(self, ranges_dir):
        if not os.path.isdir(ranges_dir):
            exit("Range_dir options is not a Directory")
        for country in os.listdir(ranges_dir):
            for line in open(os.path.join(ranges_dir, country), 'r'):
                if not line.startswith("#"):
                    try:start, end = line.split('-')
                    except ValueError:
                        sys.stderr.write("invalid range: %s\n" % line.rstrip("\n"))
                        continue
                    for ip in netaddr.iter_iprange(start, end):
                        yield ip, country

    def _iterate_ports(self, ports_file):
        if not os.path.isfile(ports_file):
            exit("Ports_file options is not a File")
        for line in open(ports_file, 'r'):
            if not line.startswith("#"):
                try:port = line.rstrip("\r\n").split(" ")[0]
                except:sys.stderr.write("invalid port: %s\n" % line)
                if len(port) > 0:
                    yield int(port)

    def _scan_batch(self, batch, timeout=10):
        for job in batch:
            self.attempts += 1
            self._send.send_syn_packet(job["source_ip"],
                                      job["dest_ip"],
                                      58124,
                                      job["dest_port"])
        self._print_status()

    def _print_status(self):
        try:
            while True:self.found += self._found_queue.get(timeout=0.001)
        except:pass
        message = "\b" * 100
        message += "sent: %s" % self.attempts
        message += "\treceived: %s" % self.found
        sys.stdout.write(message)
        sys.stdout.flush()

    def scan(self, ranges_dir, ports_file, rate):
        try:
            batch = []
            start = time.time()
            for port in self._iterate_ports(ports_file):
                for ip, country in self._iterate_ips_and_country(ranges_dir):
                    batch.append({"source_ip": self.my_ip,
                                  "dest_ip": str(ip),
                                  "dest_port": port})
                    if len(batch) >= int(rate):
                        self._scan_batch(batch)
                        batch = []
                        while time.time() - start < 1:
                            time.sleep(.1)
                        start = time.time()
            self._scan_batch(batch)
            sys.stdout.write("\nwaiting 10 sec\n")
            for x in reversed(xrange(10)):
                time.sleep(1)
        except KeyboardInterrupt:
            self.__del__()
            exit("\nbye")

    def _listen_server(self, ranges_dir, output):
        for ip, port in self._receive.yield_synack():
            banner_module = self._banner_modules[int(port)]
            banner_module.run(ip, port)

    def _collect_results(self, output):
        received = 0
        f = open(output, "a")
        for module in self._banner_modules:
            banner_module = self._banner_modules[module]
            try:
                while True:
                    result = banner_module.queue.get(timeout=0.1)
                    country = self._lookup.find(result["ip"])
                    result["country"] = country
                    received += 1
                    f.write("%s\n" % result)
            except:pass
        f.close()
        return received

    def _result_collector(self, output, queue):
        while True:
            queue.put(self._collect_results(output))
            time.sleep(5)

    def listen(self, ranges_dir, output):
        self._lookup.add_range_dir(ranges_dir)
        self.listen_server = multiprocessing.Process(
            target=self._listen_server,
            args=(ranges_dir, output))
        self.listen_server.start()
        self.result_collector = multiprocessing.Process(
            target=self._result_collector,
            args=(output, self._found_queue))
        self.result_collector.daemon = True
        self.result_collector.start()

    def __del__(self):
        try:self.listen_server.terminate()
        except:pass
        try:self.results_collector.terminate()
        except:pass

    def run(self, ranges_dir, ports_file, rate, output):
        self.listen(ranges_dir, output)
        self.scan(ranges_dir, ports_file, rate)
        self._collect_results(output)
        self._print_status()
        self.__del__()
        exit("\nbye")
