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
        self._temp_output = tempfile.mkstemp()[1]
        self.country_lookup = Country_Lookup()
        self.scan_server = Scan_Server()
        self.banners = Helper_Class()

    def _finger_print(self):
        f = open(self._temp_output, 'r')
        while True:
            try:
                line = f.readline()
                status = self.scan_server.poll()
                if line and not line.startswith("#"):
                    try:
                        args = line.split(" ")
                        result = self.banners.scan_port(args[3], args[2])
                        result['country'] = self.country_lookup.find(ip)
                        yield result
                    except Exception as e:
                        print "[ERROR] %s" % e
                else:
                    if status is not None:break
                    time.sleep(.1)
            except KeyboardInterrupt:return
            except Exception as e:
                print  "[ERROR] %s" % e

    def run(self, range_dir, port_file, rate, iface, output):
        self.country_lookup.add_range_dir(range_dir)
        self.scan_server.scan(range_dir, port_file, rate, iface, self._temp_output)
        f = open(output, 'w+')
        for result in self._finger_print():
            try:f.write("%s\n" % json.dump(result))
            except:pass
            f.flush()
        f.close()

    def __del__(self):
        try:os.remove(self._temp_output)
        except:pass
