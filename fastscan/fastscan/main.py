import os
import time
import json
import inspect
import tempfile
from banners.helper import Helper_Class
from fastscan.scan_server import Scan_Server
from fastscan.country_lookup import Country_Lookup


class Main:
    def __init__(self):
        self.country_lookup = Country_Lookup()
        self.scan_server = Scan_Server()
        self.banners = Helper_Class()
        self.mass_output = ""

    def _finger_print(self):
        while not os.path.exists(self.mass_output):
            time.sleep(1)
        f = open(self.mass_output, 'r')
        while True:
            try:
                line = f.readline()
                status = self.scan_server.poll()
                if line and not line.startswith("#"):
                    try:
                        args = line.split(" ")
                        result = self.banners.scan_port(args[3], args[2])
                        result['country'] = self.country_lookup.find(args[3])
                        yield result
                    except Exception as e:
                        print "[ERROR] %s" % e
                else:
                    if status is not None:
                        f.close()
                        break
                    time.sleep(.1)
            except KeyboardInterrupt:return
            except Exception as e:
                print  "[ERROR] %s" % e

    def run(self, range_dir, port_file, rate, iface, output):
        self.country_lookup.add_range_dir(range_dir)
        self.mass_output = "%s_masscan" % output
        self.scan_server.scan(range_dir, port_file, rate, iface, self.mass_output)
        f = open(output, 'w+')
        for result in self._finger_print():
            try:f.write("%s\n" % json.dumps(result))
            except Exception as e:print e
            f.flush()
        f.close()
