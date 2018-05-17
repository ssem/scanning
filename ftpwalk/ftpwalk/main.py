#!/usr/bin/env python
import os
import sys
import time
import ftplib


class Ftpwalk():
    def __init__(self, verbose=False):
        self.ftp = ftplib.FTP()
        self.users = ["anonymous", "root", "admin", "user"]
        self.passwds = ["anonymous", "password", "123456", "qwerty", "admin",
                        "password1", "root"]
        self.verbose = verbose

    def try_user_pass(self, user, passwd):
        try:
            if self.verbose:
                sys.stdout.write("Login: %s %s\n" % (user, passwd))
            self.ftp.login(user, passwd)
            return 0
        except ftplib.error_perm:
            if self.verbose:
                sys.stdout.write("failed\n")
            return 1
        except Exception:
            if self.verbose:
                sys.stdout.write("disconnected\n")
            return 2

    def login(self, ip, port, timeout=5):
        attempt = 0
        reconnect = 999999
        self.ftp.connect(ip, port, timeout)
        for user in self.users:
            for passwd in self.passwds:
                result = self.try_user_pass(user, passwd)
                attempt += 1
                if result == 0: # Success
                    return user, passwd
                elif result == 2: # Disconnected
                    reconnect = attempt-1
                    self.ftp.close()
                    self.ftp.connect(ip, port, timeout)
                    result = self.try_user_pass(user, passwd)
                    if result == 0:
                        return user, passwd
                if attempt >= reconnect:
                    attempt = 0
                    self.ftp.close()
                    self.ftp.connect(ip, port, timeout)
        return "unknown", "unknown"

    def _parse(self, line):
        if line[0] == "d":
            self._dirs.append(line.split()[-1])
        else:
            self._files.append(line.split()[-1])

    def walk(self, top):
        self._dirs = []
        self._files = []
        try:
            self.ftp.cwd(top)
            self.ftp.dir(top, self._parse)
            yield top, self._dirs, self._files
            for ds in self._dirs:
                for root, dirs, files in self.walk(os.path.join(top, ds)):
                    yield root, dirs, files
        except KeyboardInterrupt as e:raise(e)
        except Exception:pass

    def get_files(self, root="/"):
        results = []
        for root, dirs, files in self.walk(root):
            for f in files:
                fullpath = os.path.join(root, f)
                if self.verbose:
                    sys.stdout.write("path: %s\n" % fullpath)
                results.append(fullpath)
        return results

    def scan_port(self, ip, port, timeout=5):
        result = {"ip": ip,
                  "port": port,
                  "user": "",
                  "password": "",
                  "files": [],
                  "time": time.time()}
        try:
            user, password = self.login(ip, port, timeout)
            result["user"] = user
            result["password"] = password
            result["files"] = self.get_files()
        except KeyboardInterrupt as e:raise(e)
        except Exception as e:
            result["error"] = repr(e)
        return result
