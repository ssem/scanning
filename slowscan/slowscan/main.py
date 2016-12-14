import os
import sys
import time
from datetime import datetime
from datetime import timedelta
from slowscan.scan_server import Scan_Server
from slowscan.listen_server import Listen_Server

class Main:
    def __init__(self):
        self.scan_server = Scan_Server()
        self.listen_server = Listen_Server()

    def _print_status(self, rate):
        total = self.scan_server.total
        attempts = self.scan_server.attempts
        seconds = (total - attempts) / rate
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        estimate = "%s:%s:%s" % (h, m, s)
        try:percent = "{:.0f}%".format(float(attempts)/float(total) * 100)
        except:percent = "0%"
        sys.stdout.write("\b" * 100)
        sys.stdout.write("received: %s sent:%s total:%s percent:%s estimate:%s" % (
            self.listen_server.received, attempts, total, percent, estimate))
        sys.stdout.flush()

    def run(self, range_dir, port_file, rate, output):
        try:
            self.listen_server.listen(range_dir, output)
            self.scan_server.scan(range_dir, port_file, rate)
            while self.scan_server.is_alive():
                if output != sys.stdout:
                    self._print_status(rate)
                    time.sleep(1)
            while self.listen_server.is_alive():
                if output != sys.stdout:
                    self._print_status(rate)
                    time.sleep(1)
            sys.stdout.write("\n")
            for x in reversed(xrange(1,30)):
                if output != sys.stdout:
                    sys.stdout.write("\b" * 100)
                    sys.stdout.write("waiting %s..." % x)
                    sys.stdout.flush()
                time.sleep(1)
            self._print_status(rate)
            sys.stdout.write("\n")
        except KeyboardInterrupt:exit("bye")
