#!/usr/bin/env python
import argparse


class Nmap_Service_Probe():
    def __init__(self):
        self.services = {}

    def parse(self, nmap):
        for line in open(nmap, 'r'):
            match = {'regex_flag': '',
                     'product': '',
                     'version': '',
                     'info': '',
                     'hostname': '',
                     'os_type': '',
                     'device_type': '',
                     'cpe': ''}
            match['match'] = line.split(' ')[0]
            try:
                if match['match'] == 'match' or match['match'] == 'softmatch':
                    match['service'] = line.split(' ')[1]
                    match['regex_type'] = line.split(' ')[2][0]
                    if match['regex_type'] != 'm':
                        raise Exception('regex type != m Not Implemented')
                    match['regex_delim'] = line.split(' ')[2][1]
                    regex_offset = line.index(match['service']) + len(match['service']) + 1
                    if not line[regex_offset:].startswith('m'):
                        raise Exception('incorrect offset')
                    match['regex'] = line[regex_offset:].split(match['regex_delim'])[1]
                    template_offset = line.index(match['regex']) + len(match['regex']) + 1
                    match['regex_flag'] = line[template_offset]
                    if 'p/' in line[template_offset:]:
                        match['product'] = line[template_offset:].split('p/')[-1].split('/')[0]
                    if 'v/' in line[template_offset:]:
                        match['version'] = line[template_offset:].split('v/')[-1].split('/')[0]
                    if 'i/' in line[template_offset:]:
                        match['info'] = line[template_offset:].split('i/')[-1].split('/')[0]
                    if 'h/' in line[template_offset:]:
                        match['hostname'] = line[template_offset:].split('h/')[-1].split('/')[0]
                    if 'o/' in line[template_offset:]:
                        match['os_type'] = line[template_offset:].split('o/')[-1].split('/')[0]
                    if 'd/' in line[template_offset:]:
                        match['device_type'] = line[template_offset:].split('d/')[-1].split('/')[0]
                    if 'cpe:/' in line[template_offset:]:
                        match['cpe'] =  line[template_offset:].split('cpe:/')[-1].split('/')[0]
                    if match['service'] in self.services:
                        self.services[match['service']].append(match)
                    else:
                        self.services[match['service']] = [match]
            except: continue

    def get_all(self):
        return self.services

    def get_service(self, service):
        if service in self.services:
            return self.services[service]
        else:
            return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("nmap", help="nmap service probes file")
    parser.add_argument('--service', default="all", help="service to grab (DEFAULT:ALL)")
    args = parser.parse_args()
    nsp = Nmap_Service_Probe()
    nsp.parse(args.nmap)
    if args.service == "all":
        print nsp.get_all()
    else:
        print nsp.get_service(args.service)
