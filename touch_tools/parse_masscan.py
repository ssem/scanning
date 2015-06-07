#!/usr/bin/env python
import time
import argparse


class Parse_Masscan():
    def parse(self, masscan_file):
        for line in open(masscan_file, 'r'):
            if not line.startswith('#'):
                result = line.rstrip('\r\n').split(' ')
                yield {'status': result[0],
                       'protocol': result[1],
                       'port': result[2],
                       'ip': result[3],
                       'time': time.strftime('%d %b %y %H:%M:%S', time.localtime(float(result[4])))}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mass", help="masscan file")
    args = parser.parse_args()
    pm = Parse_Masscan()
    for ip in pm.parse(args.mass):
        print ip
