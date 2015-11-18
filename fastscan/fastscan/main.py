import os
import time
import inspect
import tempfile
from banners.helper import Helper_Class
from fastscan.scan_server import Scan_Server
from fastscan.country_lookup import Country_Lookup


class Main:
    def __init__(self):
        self._temp_output = tempfile.mkstemp()[1]
        self.country_lookup = Country_Lookup()
        self.scan_server = Scan_Server()
        self.banners = Helper_Class()

    def _finger_print(self):
        f = open(self._temp_output, 'r')
        while True:
            line = f.readline()
            status = self.scan_server.poll()
            if line and not line.startswith("#"):
                try:
                    args = line.split(" ")
                    ip = args[3]
                    port = args[2]
                except: continue
                result = self.banners.scan_port(ip, port)
                if result != None:
                    result['country'] = self.country_lookup.find(ip)
                    yield result
            else:
                if status is not None:
                    break
                time.sleep(.1)

    def run(self, range_dir, port_file, rate, output):
        self.country_lookup.add_range_dir(range_dir)
        self.scan_server.scan(range_dir, port_file, rate, self._temp_output)
        f = open(output, 'w+')
        for result in self._finger_print():
            f.write("%s\n" % result)
            f.flush()
        f.close()

    def __del__(self):
        try:os.remove(self._temp_output)
        except:pass
