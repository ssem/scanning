import os
import json
import time
import tempfile
from subprocess import PIPE
from subprocess import Popen


class Bruteforce:
    def __init__(self):
        self.output = tempfile.mkstemp()[1]

    def __del__(self):
        try:os.remove(self.output)
        except:pass

    def _get_results(self):
        fh = open(self.output, "r")
        try:
            obj = json.loads(fh.read())
            return json.dumps(obj["results"][0])
        except:pass
        fh.close()
        return None

    def run(self, target, port, proto, userfile, passfile, parallel="16", 
                  connection_timeout="3", total_timeout="9999999"):
        cmd = ["hydra", target, "-s", port, "-o", self.output, "-L", userfile, 
               "-P", passfile, "-b", "json", "-w", connection_timeout, 
               "-e", "ns", "-u", "-f", "-t", parallel, proto]
        p = Popen(cmd,)# stdout=PIPE, stderr=PIPE) 
        start = time.time()
        total_timeout = int(total_timeout)
        while (time.time() - start) < total_timeout:
            time.sleep(.1)
            if p.poll() != None:
                break
        try:p.terminate()
        except:pass
        try:p.kill()
        except:pass
        return self._get_results()
