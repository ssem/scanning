#!/usr/bin/env python
import os
import sys
import json
import time
import socket
import inspect
import argparse
import requests


class Parent():
    def __init__(self):
        self.blacklist_ips = []

    def run(self, ip, port, timeout=10):
        if ip not in self.blacklist_ips:
            try:banner = self.get_banner(ip, port, timeout)
            except:banner = None
            if banner is not None and banner is not "":
                banner = banner.rstrip('\r\n')
                exploit = self.check_banner(banner)
                return {"ip": ip,
                        "port": port,
                        "banner": banner,
                        "exploit": exploit,
                        "time": time.time()}
        return None

    def get_banner(self, ip, port, timeout=10):
        raise Exception('Not Implemented')

    def check_banner(self, banner):
        raise Exception('Not Implemented')

class HoneyPot(Parent):
    default_port = 0

    def get_banner(self, ip, port, timeout=10):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(int(timeout))
        s.connect((ip, int(port)))
        s.send('/')
        banner = s.recv(100)
        s.close()
        return banner

    def check_banner(self, banner):
        return 'Honeypot'

class Chargen(Parent):
    default_port = 19

    def get_banner(self, ip, port, timeout=10):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(int(timeout))
        s.connect((ip, int(port)))
        banner = s.recv(10)
        s.close()
        return banner

    def check_banner(self, banner):
        return 'OSVDB 150'

class Ftp(Parent):
    default_port = 21

    def get_banner(self, ip, port, timeout=10):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(int(timeout))
        s.connect((ip, int(port)))
        banner = s.recv(4096)
        s.close()
        return banner

    def check_banner(self, banner):
        if "ProFTPD 1.3" in banner:
            return "OSVDB 68985"
        elif "Pure-FTPd" in banner:
            return "OSVDB 112004"
        elif "Version wu-2" in banner:
            return 'OSVDB 11805'
        elif "Webstar" in banner:
            return "OSVDB 7794"
        elif "(vsFTPd 2.3.4)" in banner:
            return "OSVDB 73573"
        elif '3Com 3CDaemon FTP' in banner:
            return 'OSVDB 12811'
        elif 'Ability FTP' in banner:
            return 'OSVDB 11030'
        elif 'AbsoluteFTP' in banner:
            return 'OSVDB 77105'
        elif 'CasarFTP 0.99g' in banner:
            return 'OSVDB 26364'
        elif "\x32\x32\x30\x20\xbb\xb6\xd3\xad\xb9\xe2\xc1\xd9\x46" in banner:
            return 'OSVDB 82798'
        elif 'Dream FTP Server' in banner:
            return 'OSVBD 4986'
        elif 'Easy File Sharing FTP Server' in banner:
            return 'OSVDB 27646'
        elif 'BigFoolCat' in banner:
            return 'OSVDB 62134'
        elif 'FileCOPA FTP' in banner:
            return 'OSVDB 27389'
        elif 'FreeFloat' in banner:
            return 'OSVDB 69621'
        elif 'freeFTPd 1.0' in banner:
            return 'OSVDB 96517'
        elif 'GlobalSCAPE Secure FTP' in banner:
            return 'OSVDB 16049'
        elif 'Golden FTP Server ready v4' in banner:
            return 'OSVDB 35951'
        elif 'httpdx' in banner:
            return 'OSVDB 60181'
        elif 'Microsoft IIS ftp' in banner:
            return 'OSVDB 57589'
        elif 'NetTerm FTP server' in banner:
            return 'OSVDB 15865'
        elif 'odin FTP server' in banner:
            return 'OSVDB 68824'
        elif '**        Welcome on       **' in banner:
            return 'OSVDB 65687'
        elif "PCMan's FTP Server 2.0" in banner:
            return 'OSVDB 94624'
        elif 'quickshare ftpd' in banner:
            return 'OSVDB 70776'
        elif 'DSC ftpd 1.0 FTP Server' in banner:
            return 'OSVDB 79691'
        elif 'Serv-U FTP Server v4' in banner:
            return 'OSVDB 3713'
        elif 'SlimFTPd' in banner:
            return 'OSVDB 18172'
        elif 'TurboFTP Server 1.30' in banner:
            return 'OSVDB 85887'
        elif 'vftpd' in banner:
            return 'OSVDB 62163'
        elif 'XLINK FTP Server' in banner:
            return 'OSVDB 58646'
        elif 'nas4free FTP Server' in banner:
            return 'CVE 2013-3631'
        elif 'SurgeFTP' in banner:
            return 'OSVDB 89105'
        elif 'OpenMediaVault' in banner:
            return 'CVE 2013-3632'
        else:
            return ""

class Ssh(Parent):
    default_port = 22

    def get_banner(self, ip, port, timeout=10):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(int(timeout))
        s.connect((ip, int(port)))
        banner = s.recv(4096)
        s.close()
        return banner

    def check_banner(self, banner):
        if 'Tectia Server' in banner:
            return 'OSVDB 88103'
        elif 'ArrayOS' in banner:
            return 'OSVDB 104654'
        elif 'SysaxSSH' in banner:
            return 'OSVBD 79689'
        elif 'WeOnlyDo-wodFTPD 2.1.8.98' in banner:
            return 'OSVBD 25569'
        elif 'WeOnlyDo-wodFTPD 2.0.6' in banner:
            return 'OSVDB 88006'
        elif 'WeOnlyDo-wodFTPD 2.1.3' in banner:
            return 'OSVDB 88006'
        else:
            return ''

class Telnet(Parent):
    default_port = 23

    def get_banner(self, ip, port, timeout=10):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(int(timeout))
        s.connect((ip, int(port)))
        banner = s.recv(4096)
        s.close()
        return banner

    def check_banner(self, banner):
        if 'FreeBSD/' in banner:
            return 'OSVDB 78020'
        elif 'Welcome to Solaris' in banner:
            return 'OSVDB 31881'
        elif 'SunOs ' in banner:
            return 'OSVDB 690'
        elif 'TelSrv 1.5' in banner:
            return 'OSVDB 373'
        elif 'Welcome to GoodTech' in banner:
            return 'OSVDB 14806'
        else:
            return ''

class Smtp(Parent):
    default_port = 25

    def get_banner(self, ip, port, timeout=10):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(int(timeout))
        s.connect((ip, int(port)))
        banner = s.recv(4096)
        s.close()
        return banner

    def check_banner(self, banner):
        if 'Exim' in banner:
            return 'OSVDB 69685'
        elif 'ESMTP TABS Mail Server for Windows NT' in banner:
            return 'OSVDB 11174'
        elif 'Windows E-mail Server From NJStar Software' in banner:
            return 'OSVDB 76728'
        elif 'YahooPOPs! Simple Mail Transfer Service Ready' in banner:
            return 'OSVDB 10367'
        elif 'Microsoft Exchange' in banner:
            return 'OSVDB 2674'
        elif 'Dovecot' in banner:
            return 'OSVDB 93004'
        elif 'OK POP3 server' in banner:
            return 'OSVDB 11975'
        elif 'Cyrus' in banner:
            return 'OSVDB 25853'
        elif 'IMAP4rev1 v12.264' in banner:
            return 'OSVDB 12037'
        elif 'WorldMail' in banner:
            return 'OSVDB 22097'
        elif 'MailEnable' in banner and '2.34' in banner:
            return 'OSVDB 32125'
        elif 'MailEnable' in banner and '2.35' in banner:
            return 'OSVDB 32124'
        elif 'MailEnable' in banner and '1.54' in banner:
            return 'OSVDB 17844'
        elif 'MDaemon 8.0.3' in banner:
            return 'OSVDB 11838'
        elif 'MDaemon 9.6.4' in banner:
            return 'OSVDB 43111'
        elif 'MERCUR' in banner and 'v5.00' in banner:
            return 'OSVDB 23950'
        elif 'Mercury/32' in banner:
            return 'OSVDB 33883'
        elif 'NetMail' in banner:
            return 'OSVDB 31362'
        else:
            return ''

class Http(Parent):
    default_port = 80

    def get_banner(self, ip, port, timeout=10):
        banner = ''
        r = requests.get('http://%s:%s' % (ip, port), timeout=float(timeout))
        for field in r.headers:
            banner += '%s: %s\n' % (field, r.headers[field])
        banner += r.content[:100]
        return banner

    def check_banner(self, banner):
        if 'Symantec Messaging Gateway' in banner:
            return 'OSVDB 85028'
        elif 'AjaXplorer=' in banner:
            return 'OSVDB 63552'
        elif 'CUPS/' in banner:
            return 'CVE 2014-6271'
        elif 'X-Powered-By: Coldfusion' in banner:
            return 'CVE 2013-0632'
        elif 'drupal' in banner.lower():
            return 'CVE 2014-3704'
        elif 'eXtplorer=' in banner:
            return 'OSVDB 88751'
        elif 'realm="GestioIP"' in banner:
            return 'OSVDB 98245'
        elif 'GlassFish' in banner:
            return 'OSVDB 71948'
        elif 'Horde=' in banner:
            return 'OSVDB 79246'
        elif 'SiteScope/' in banner:
            return 'OSVDB 99230'
        elif 'ispconfig/lighttpd' in banner:
            return 'CVE 2013-3629'
        elif 'JBoss' in banner:
            return 'OSVDB 64171'
        elif 'X-Jenkins' in banner:
            return 'EDB 24272'
        elif 'MobileCartly' in banner:
            return 'OSVDB 85509'
        elif 'MoodleSession=' in banner:
            return 'CVE 2013-3630'
        elif 'Mutiny : Login @ mutiny' in banner:
            return 'OSVDB 86570'
        elif 'realm="op5"' in banner:
            return 'OSVDB 78065'
        elif 'Pandora' in banner and 'v3.1 Build PC10060' in banner:
            return 'OSVDB 69549'
        elif 'phpLDAPadmin 1.2' in banner:
            return 'OSVDB 76594'
        elif 'phpMyAdmin=' in banner:
            return 'OSVDB 85739'
        elif 'PHPTAX by William L' in banner:
            return 'OSVDB 86992'
        elif 'qdpm=' in banner:
            return 'OSVDB 82978'
        elif 'www.thebonnotgang.com' in banner:
            return 'OSVDB 83767'
        elif 'SiT! Support Incident Tracker' in banner:
            return 'OSVDB 76999'
        elif 'Splunk Inc. Splunk' in banner:
            return 'OSVDB 77695'
        elif 'Sun Java System' in banner:
            return 'OSVDB 61851'
        elif 'TestLink 1.9.3' in banner:
            return  'OSVDB 85446'
        elif 'WebPagetest - Website Performance' in banner:
            return 'OSVDB 83822'
        elif 'Powered by WikkaWiki' in banner:
            return 'OSVDB 77393'
        elif 'This program makes use of the Zend' in banner:
            return 'OSVDB 25149'
        elif 'Zavvix 2.0' in banner:
            return 'CVE 2013-3628'
        elif 'Novell ZENworks Control Center' in banner:
            return 'OSVDB 91627'
        elif 'realm="EvoCam"' in banner:
            return 'OSVDB 65043'
        elif 'realm="Skyrouter"' in banner:
            return 'OSVDB 77497'
        elif 'FreePBX' in banner:
            return 'OSVDB 80544'
        elif 'SecurityGateway' in banner:
            return 'OSVDB 45854'
        elif "request that this server didn't understand" in banner:
            return 'OSVDB 66814'
        elif 'Oracle HTTP Server Powered by' in banner:
            return 'OSVDB 838'
        elif 'BadBlue 2.5' in banner:
            return 'OSVDB 14238'
        elif 'BEA WebLogic' in banner:
            return 'OSVDB 47096'
        elif 'ManageEngine Desktop Central' in banner:
            return 'OSVDB 100008'
        elif 'Easy-Web Server' in banner:
            return 'OSVDB 66614'
        elif 'Ericom AccessNow Server' in banner:
            return 'CVE 2014-3913'
        elif 'HP Managed Printing Administration' in banner:
            return 'OSVBD 78-15'
        elif 'httpdx' in banner and 'Win32' in banner:
            return 'OSVDB 58714'
        elif 'Icecast ' in banner:
            return 'OSVDB 10406'
        elif 'intrasrv 1.0' in banner:
            return 'OSVDB 94097'
        elif 'Ipswitch-IMail/8.03' in banner:
            return 'OSVDB 9177'
        elif 'content="JIRA"' in banner:
            return 'OSVDB 103807'
        elif 'Kaseya-Tetra' in banner:
            return 'OSVDB 99984'
        elif 'Kolibri-2.0' in banner:
            return 'OSVDB 70808'
        elif 'LANDesk Management Agent' in banner:
            return 'OSVDB 79276'
        elif 'MarkVision Enterprise' in banner:
            return 'CVE 2014-8741'
        elif 'MailEnable' in banner:
            return 'OSVDB 15913'
        elif 'Spipe 1.0' in banner:
            return 'OSVDB 29421'
        elif 'WDaemon 6.8' in banner:
            return 'OSVDB 3255'
        elif 'MiniWeb' in banner:
            return 'OSVDB 92198'
        elif '2.01 11th September' in banner:
            return 'OSVDB 29257'
        elif 'NetDecision-HTTP-Server 1.0' in banner:
            return 'OSVDB 79651'
        elif 'peercast=' in banner:
            return 'OSVDB 23777'
        elif 'PrivateWire GateWay' in banner:
            return 'OSVDB 26861'
        elif 'PSO Proxy 0.9' in banner:
            return 'OSVDB 4028'
        elif 'R4 Embedded Server' in banner:
            return 'OSVDB 79007'
        elif 'server: hfs' in banner.lower():
            return 'OSVDB 111386'
        elif 'server: sambar' in banner.lower():
            return 'OSVDB 5786'
        elif 'Savant 3.1' in banner:
            return 'OSVDB 9829'
        elif 'Serv-U' in banner:
            return 'OSVDB 59772'
        elif 'Network Audio Server' in banner:
            return '12585'
        elif 'SHTTPD' in banner:
            return 'OSVDB 29565'
        elif 'SolarWinds - Storage Manager' in banner:
            return 'OSVDB 81634'
        elif 'Scrutinizer 9.' in banner:
            return 'OSVDB 84232'
        elif 'Steamcast 0.9.75' in banner:
            return 'OSVDB 42670'
        elif 'PMSoftware-SWS 2.' in banner:
            return 'OSVDB 84310'
        elif 'EAServer' in banner:
            return 'OSVDB 17996'
        elif 'Center Chargeback Manager' in banner:
            return 'OSVDB 94188'
        elif 'Xitami' in banner:
            return 'OSVDB 40594'
        elif 'Alcatel Cloud DVR Streamer' in banner:
            return 'OSVDB 40521'
        elif 'direct entry from outside' in banner:
            return 'OSVDB 88860'
        elif 'Basic realm="DD-WRT"' in banner:
            return 'OSVDB 55990'
        elif 'DIR-645' in banner:
            return 'OSVDB 95951'
        elif 'DIR-600' in banner or 'DIR-300' in banner:
            return 'OSVDB 89861'
        elif 'DIR-815' in banner:
            return 'OSVDB 92144'
        elif 'DIR-605' in banner:
            return 'OSVDB 86824'
        elif 'DIR-615' in banner:
            return 'OSVDB 90174'
        elif 'Dolibarr 3.1.1' in banner:
            return 'OSVDB 80980'
        elif 'GroundWork' in banner:
            return 'OSVDB 91051'
        elif 'HP System Management Homepage v' in banner:
            return 'OSVDB 91912'
        elif 'realm="WRT54G"' in banner or 'realm="WRT54GS"' in banner:
            return 'OSVDB 19389'
        elif 'realm="E1500"' in banner:
            return 'OSVDB 89912'
        elif 'realm="Linksys E2500"' in banner:
            return 'OSVDB 89912'
        elif 'realm="Linksys E4200"' in banner:
            return 'OSVDB 103321'
        elif 'realm="Linksys E2100L"' in banner:
            return 'OSVDB 103321'
        elif 'realm="Linksys E2000"' in banner:
            return 'OSVDB 103321'
        elif 'realm="Linksys E1550"' in banner:
            return 'OSVDB 103321'
        elif 'realm="E1200"' in banner:
            return 'OSVDB 103321'
        elif 'realm="E1000"' in banner:
            return 'OSVDB 103321'
        elif 'realm="E900"' in banner:
            return 'OSVDB 103321'
        elif 'realm="WRT110"' in banner:
            return 'CVE 2013-3568'
        elif 'realm="WRT160Nv2"' in banner:
            return 'OSVDB 90093'
        elif 'realm="WRT54GL"' in banner:
            return 'OSVDB 89912'
        elif 'JSESSIONID=' in banner:
            return 'OSVDB 93444'
        elif 'realm="NETGEAR DGN1000B"' in banner:
            return 'OSVDB 89985'
        elif 'realm="NETGEAR DGN2200B"' in banner:
            return 'OSVDB 90320'
        elif 'nginx/1.3.9' in banner or 'nginx/1.4.0' in banner:
            return 'OSVDB 93037'
        elif 'Openfiler Storage' in banner:
            return 'OSVDB 93881'
        elif 'Symantec Web Gateway' in banner:
            return 'OSVDB 82925'
        elif 'V-CMS v1' in banner:
            return 'OSVDB 77183'
        elif 'WebCalendar v1.2' in banner:
            return 'OSVDB 81329'
        elif 'Openfire, ' in banner:
            return 'OSVDB 49663'
        else:
            return ''

class Mcafee(Http):
    default_port = 81

    def check_banner(self, banner):
        if 'Spipe 1.0' in banner:
            return 'OSVDB 29421'

class Remote_Telnet(Parent):
    default_port = 107

    def get_banner(self, ip, port, timeout=10):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(int(timeout))
        s.connect((ip, int(port)))
        banner = s.recv(4096)
        s.close()
        return banner

    def check_banner(self, banner):
        if 'FreeBSD/' in banner:
            return 'OSVDB 78020'
        elif 'Welcome to Solaris' in banner:
            return 'OSVDB 31881'
        elif 'SunOs ' in banner:
            return 'OSVDB 690'
        elif 'TelSrv 1.5' in banner:
            return 'OSVDB 373'
        elif 'Welcome to GoodTech' in banner:
            return 'OSVDB 14806'
        else:
            return ''

class Pop3(Smtp):
    default_port = 110

class Imap(Smtp):
    default_port = 143

class Https(Http):
    default_port = 443

    def get_banner(self, ip, port, timeout=10):
        banner = ''
        r = requests.get(
            url='https://%s:%s' % (ip, port),
            verify=False,
            timeout=float(timeout))
        for field in r.headers:
            banner += '%s:%s\n' % (field, r.headers[field])
        banner += r.content[:100]
        return banner

#class Smb(Parent):
#    default_port = 445

#class Modbus(Parent):
#    default_port = 502

#class Rexec(Parent):
#    default_port = 512

#class Rlogin(Parent):
#    default_port = 513

#class Rsh(Parent):
#    default_port = 514

#class Db2(Parent):
#    default_port = 523

#class Apple_File_Protocol(Parent):
#    default_port = 548

class Cups(Http):
    default_port = 631

    def check_banner(self, banner):
        if 'CUPS/' in banner:
            return 'CVE 2014-6271'
        else:
            return ''

#class Rsync(Parent):
#    default_port = 873

#    def get_banner(self, ip, port, timeout=10):
#        try:
#            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#            s.settimeout(int(timeout))
#            s.connect((ip, int(port)))
#            s.send('/')
#            banner = s.recv(4096)
#            s.close()
#            return banner, ''
#        except Exception as e:print '\n%s\n' % e

#class Vmauthd(Parent):
#    default_port = 902
#
#    def get_banner(self, ip, port, timeout=10):
#        try:
#            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#            s.settimeout(int(timeout))
#            s.connect((ip, int(port)))
#            banner = s.recv(4096)
#            s.close()
#            return banner, ''
#        except Exception as e:print '\n%s\n' % e

#class Zenworks(Parent):
#    default_port = 998

#class Java_Rmi(Parent):
#    default_port = 1099

#class Sap_Host(Parent):
#    default_port = 1128

#class Sid(Parent):
#    default_port = 1158

#class Nj_Rat(Parent):
#    default_port = 1170

#class Nessus(Parent):
#    default_port = 1241

#class Jrat(Parent):
#    default_port = 1336

#class Tns(Parent):
#    default_port = 1521

#class Dark_Comet(Parent):
#    default_port = 1604

#class H323(Parent):
#    default_port = 1720

#class Network_file_system(Parent):
#    default_port = 2049

#class Dlsw(Parent):
#    default_port = 2067

#class Digi(Parent):
#    default_port = 2362

class GoodTech(Parent):
    default_port = 2380

    def get_banner(self, ip, port, timeout):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(int(timeout))
        s.connect((ip, int(port)))
        banner = s.recv(4096)
        s.close()
        return banner

    def check_banner(self, banner):
        if 'Welcome to GoodTech' in banner:
            return 'OSVDB 14806'
        else:
            return ''

class Hp_Management(Http):
    default_port = 2381

    def check_banner(self, banner):
        if 'HP System Management Homepage v' in banner:
            return 'OSVDB 91912'
        else:
            return ''

class Mdaemon(Http):
    default_port = 3000

    def check_banner(self, banner):
        if 'WDaemon 6.8' in banner:
            return 'OSVDB 3255'
        else:
            return ''

#class Novell(Parent):
#    default_port = 3037

#class Ib(Parent):
#    default_port = 3050

#class Apple_Remote_Desktop(Parent):
#    default_port = 3283

#class Sap_Router(Parent):
#    default_port = 3299

#class Mysql(Parent):
#    default_port = 3306

#class Posion_Ivy(Parent):
#    default_port = 3460

#class RTMP(Parent):
#    default_port = 3500

#class Nexpose(Parent):
#    default_port = 3780

#class Msf(Parent):
#    default_port = 3790

class AltN(Http):
    default_port = 4000

    def check_banner(self, banner):
        if 'SecurityGateway' in banner:
            return 'OSVDB 45854'
        else:
            return ''

#class Sockso(Parent):
#    default_port = 4444

#class Kademlia(Parent):
#    default_port = 4672

class Eaton_Network(Http):
    default_port = 4679

    def check_banner(self, banner):
        if 'This program makes use of the Zend' in banner:
            return 'OSVDB 25149'
        else:
            return ''

class GlassFish(Http):
    default_port = 4848

    def check_banner(self, banner):
        if 'GlassFish' in banner:
            return 'OSVDB 71948'
        else:
            return ''

#class Windows_Deployment(Parent):
#    default_port = 5040

#class Sip(Parent):
#    default_port = 5060

#class Postgres(Parent):
#    default_port = 5432

#class IsqlPlus(Parent):
#    default_port = 5560

#class Pcanywhere(Parent):
#    default_port = 5631

#class Vnc(Parent):
#    default_port = 5900
#
#    def get_banner(self, ip, port, timeout=10):
#        try:
#            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#            s.settimeout(int(timeout))
#            s.connect((ip, int(port)))
#            banner = s.recv(4096)
#            s.close()
#            return banner, ''
#        except Exception as e:print '\n%s\n' % e

#class Cctv(Parent):
#    default_port = 5920

#class CouchDb(Parent):
#    default_port = 5984

#class X11(Parent):
#    default_port = 6000

#class Manage_Engine(Parent):
#    default_port = 6060

#class Dameware(Parent):
#    default_port = 6129

class vsftp(Parent):
    default_port = 6200

    def get_banner(self, ip, port, timeout):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(int(timeout))
        s.connect((ip, int(port)))
        banner = s.recv(4096)
        s.close()
        return banner

    def check_banner(self, banner):
        if "(vsFTPd 2.3.4)" in banner:
            return "OSVDB 73573"
        else:
            return ''

#class Redis(Parent):
#    default_port = 6379

#class InfoPage_Svr(Parent):
#    default_port = 6405

#class Groupwise(Parent):
#    default_port = 7181

class Netwin(Http):
    default_port = 7021

    def check_banner(self, banner):
        if 'SurgeFTP' in banner:
            return 'OSVDB 89105'
        else:
            return ''

class Peercast(Http):
    default_port = 7144

    def check_banner(self, banner):
        if 'peercast=' in banner:
            return 'OSVDB 23777'
        else:
            return ''


#class Energizer(Parent):
#    default_port = 7777

#class Soap(Parent):
#    default_port = 8000

#class ChromeCast(Parent):
#    default_port = 8008

class ManageEngine_Central(Http):
    default_port = 8020

    def check_banner(self, banner):
        if 'ManageEngine Desktop Central' in banner:
            return 'OSVDB 100008'
        else:
            return ''

class Http_Alternative(Http):
    default_port = 8080

#class Influxdb(Parent):
#    default_port = 8086

#class Net_Decision(Parent):
#    default_port = 8087

#class Atlassian(Parent):
#    default_port = 8095

#class Apache(Parent):
#    default_port = 8161

#class Vmware_Server(Parent):
#    default_port = 8222

class ManageEngine(Http):
    default_port = 8400

    def check_banner(self, banner):
        if 'ManageEngine Desktop Central' in banner:
            return 'OSVDB 100008'
        else:
            return ''

#class Nessus(Parent):
#    default_port = 8834

class Http_Alternative2(Http):
    default_port = 8888

#class Raysharp(Parent):
#    default_port = 9000

#class Vmware_Vcenter(Parent):
#    default_port = 9084

class OpenFire(Http):
    default_port = 9090

    def check_banner(self, banner):
        if 'Openfire, ' in banner:
            return 'OSVDB 49663'
        else:
            return ''

#class Indices(Parent):
#    default_port = 9200

#class Openvas(Parent):
#    default_port = 9390

#class QuickTime(Parent):
#    default_port = 9391

class Lexmark(Http):
    default_port = 9788

    def check_banner(self, banner):
        if 'MarkVision Enterprise' in banner:
            return 'CVE 2014-8741'
        else:
            return ''

#class Lantronix(Http):
#    default_port = 9999

#class Jspy(Parent):
#    default_port = 10001

#class Netbus(Parent):
#    default_port = 12345

#class Rosewill(Parent):
#    default_port = 13364

#class Wdbrpc(Parent):
#    default_port = 17185

#class Steam(Parent):
#    default_port = 27015

#class MongoDb(Parent):
#    default_port = 27017

#class Sub7(Parent):
#    default_port = 27374

#class Quake(Parent):
#    default_port = 27960

#class Koyo(Parent):
#    default_port = 28784

#class Lantronix_Discovery(Parent):
#    default_port = 30718

#class Titen_Fto(Parent):
#    default_port = 31001

#class Back_Orfice(Parent):
#    default_port = 31337

#class Sercomm(Parent):
#    default_port = 32764

#class Symantic(Parent):
#    default_port = 41080

#class Sielco(Parent):
#    default_port = 46824

#class Smt(Parent):
#    default_port = 49152

#class SubSari(Parent):
#    default_port = 50000

#class Sap_Management(Parent):
#    default_port = 50013

#class Msf_Rpc(Parent):
#    default_port = 55553
