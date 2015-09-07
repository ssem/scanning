import os
import sys
import tempfile
import subprocess

class Scan_Server:
    def __init__(self):
        self._temp_ranges = None
        self._temp_output = None
        self._process = None

    def _get_ranges(self, ranges_dir):
        temp_path = tempfile.mkstemp()[1]
        temp_ranges = open(temp_path, 'w')
        if not os.path.isdir(ranges_dir):
            exit("Range_dir options is not a Directory")
        for country in os.listdir(ranges_dir):
            for line in open(os.path.join(ranges_dir, country), 'r'):
                if not line.startswith("#"):
                    temp_ranges.write(line)
        temp_ranges.close()
        return temp_path

    def _get_ports(self, ports_file):
        ports = []
        if not os.path.isfile(ports_file):
            exit("Ports_file options is not a File")
        for line in open(ports_file, 'r'):
            if not line.startswith("#"):
                try:
                    port = line.rstrip("\r\n").split(" ")[0]
                    if len(port) > 0:
                        ports.append(str(port))
                except Exception as e:
                    sys.stderr.write(str(e))
        return ",".join(ports)

    def scan(self, ranges_dir, port_file, rate, output):
        self._temp_ranges = self._get_ranges(ranges_dir)
        ports = self._get_ports(port_file)
        self._temp_output = tempfile.mkstemp()[1]
        self._masscan(ports, self._temp_ranges, rate, output)

    def _masscan(self, ports, ranges, rate, output):
        print 'masscan',
        print '--exclude', '255.255.255.255',
        print '-p', ports,
        print '-iL', ranges,
        print '--rate', rate,
        print '-oL', output,
        print '--connection-timeout', '100'
        self._process = subprocess.Popen(['masscan',
            '--exclude', '255.255.255.255',
            '-p', ports,
            '-iL', ranges,
            '--rate', str(rate),
            '-oL', output,
            '--connection-timeout', '100'])

    def poll(self):
        return self._process.poll()

    def wait(self):
        return self._process.wait()

    def kill(self):
        try:return self._process.kill()
        except:pass

    def __del__(self):
        try:os.remove(self._temp_ranges)
        except:pass
        try:os.remove(self._temp_output)
        except:pass
