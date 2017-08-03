import os
import sys
import time
import json
import inspect
import tempfile
from ftpwalk.main import Ftpwalk
from brutetelnet.main import Brutetelnet
from banners.helper import Helper_Class
from fastscan.scan_server import Scan_Server
from fastscan.country_lookup import Country_Lookup


class Main:
    def __init__(self):
        self.country_lookup = Country_Lookup()
        self.scan_server = Scan_Server()
        self.banners = Helper_Class()
        self.ftpwalk = Ftpwalk()
        self.btelnet = Brutetelnet()
        self.mass_output = ""
        self.already_scanned = {}
        self.last_check=False

    def _is_masscan_running(self):
        status = self.scan_server.poll()
        if status != None and self.last_check != False:
            return False
        if status != None:
            self.last_check=True
        return True

    def _get_ip_and_port(self):
        for line in open(self.mass_output, 'r'):
            try:
                args = line.split(" ")
                ip_port = "%s:%s" % (args[3], args[2])
                if ip_port not in self.already_scanned:
                    self.already_scanned[ip_port] = ""
                    yield args[3], args[2]
            except IndexError:pass
            except Exception as e:
                sys.stdout.write(repr(e))
                sys.stdout.write("\n[Error] Parsing ip & port\n")

    def _finger_print(self, flags=[]):
        scanned = {}
        while not os.path.exists(self.mass_output):time.sleep(1)
        while self._is_masscan_running():
            for ip, port in self._get_ip_and_port():
                result = {'ip': ip,
                          'port': port,
                          'time': time.time(),
                          'country': self.country_lookup.find(ip)}
                if "verbose" in flags:
                    print result
                if "banner" in flags:
                    try:
                        tmp = self.banners.scan_port(ip, port)
                        result["banner"] = tmp["banner"]
                        result["exploit"] = tmp["exploit"]
                        result["category"] = tmp["category"]
                    except Exception as e:
                        sys.stdout.write("%s\n[ERROR] Banner\n" % e)
                if "ftpwalk" in flags:
                    try:
                        tmp = self.ftpwalk.scan_port(ip, port)
                        result["ftp user"] = tmp["user"]
                        result["ftp password"] = tmp["password"]
                        result["files"] = tmp["files"]
                    except Exception as e:
                        sys.stdout.write("%s\n[ERROR] ftpwalk\n" % e)
                if "telnet" in flags:
                    try:
                        tmp = self.btelnet.scan_port(ip, port)
                        result["telnet user"] = tmp["user"]
                        result["telnet password"] = tmp["password"]
                    except Exception as e:
                        sys.stdout.write("%s\n[ERROR] telnet\n" % e)
                if "verbose" in flags:
                    print result
                yield result
            time.sleep(2)

    def run(self, range_dir, port_file, rate, iface, output, flags=[]):
        self.country_lookup.add_range_dir(range_dir)
        self.mass_output = "%s_masscan" % output
        self.scan_server.scan(range_dir, port_file, rate, iface, self.mass_output)
        f = open(output, 'w+')
        for result in self._finger_print(flags):
            try:f.write("%s\n" % json.dumps(result))
            except Exception as e:print e
            f.flush()
        f.close()
