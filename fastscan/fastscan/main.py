import os
import time
import inspect
import tempfile
from fastscan import banners
from fastscan.scan_server import Scan_Server
from fastscan.country_lookup import Country_Lookup


class Main:
    def __init__(self):
        self._temp_output = tempfile.mkstemp()[1]
        self.country_lookup = Country_Lookup()
        self.scan_server = Scan_Server()

    def _import_banners(self, range_dir):
        banner_modules = {}
        classmembers = inspect.getmembers(banners, inspect.isclass)
        for classmember in classmembers:
            if classmember[0] != "Parent" and classmember[0] != "Process":
                cm = classmember[1]()
                banner_modules[int(cm.default_port)] = cm
        return banner_modules

    def _finger_print(self, banner_modules):
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
                banner_module = banner_modules[int(port)]
                result = banner_module.run(ip, port)
                if result:
                    result['country'] = self.country_lookup.find(ip)
                    yield result
            else:
                if status is not None:
                    break
                time.sleep(.1)

    def run(self, range_dir, port_file, rate, output):
        self.country_lookup.add_range_dir(range_dir)
        banner_modules = self._import_banners(range_dir)
        self.scan_server.scan(range_dir, port_file, rate, self._temp_output)
        f = open(output, 'w+')
        for result in self._finger_print(banner_modules):
            f.write("%s\n" % result)
            f.flush()
        f.close()

    def __del__(self):
        try:os.remove(self._temp_output)
        except:pass
