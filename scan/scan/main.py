import os
import sys
import time
from scan.scan_server import Scan_Server
from scan.listen_server import Listen_Server

class Main:
    def __init__(self):
        self.scan_server = Scan_Server()
        self.listen_server = Listen_Server()

    def _print_status(self):
        total = self.scan_server.total
        attempts = self.scan_server.attempts
        try:percent = "{:.0f}%".format(float(attempts)/float(total) * 100)
        except:percent = "0%"
        sys.stdout.write("\b" * 100)
        sys.stdout.write("received: %s sent:%s total:%s percent:%s" % (
            self.listen_server.received, attempts, total, percent))
        sys.stdout.flush()

    def run(self, range_dir, port_file, rate, outfile):
        try:
            self.listen_server.listen(range_dir, outfile)
            self.scan_server.scan(range_dir, port_file, rate)
            while self.scan_server.is_alive():
                self._print_status()
                time.sleep(1)
            sys.stdout.write("\n")
            for x in reversed(xrange(1,5)):
                sys.stdout.write("\b" * 100)
                sys.stdout.write("waiting %s..." % x)
                sys.stdout.flush()
                time.sleep(1)
            self._print_status()
            sys.stdout.write("\n")
            os.chmod(outfile, 0666)
        except KeyboardInterrupt:exit()
