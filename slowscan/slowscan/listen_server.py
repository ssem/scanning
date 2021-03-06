import time
import inspect
import argparse
import threading
import multiprocessing
from banners.helper import Helper_Class
from slowscan.raw_sock import Receive
from slowscan.country_lookup import Country_Lookup


class Listen_Server:
    def __init__(self):
        self.listen_server = None
        self._receive = Receive()
        self._received_q = multiprocessing.Queue()
        self._done = multiprocessing.Queue()
        self._received = 0

    @property
    def received(self):
        while not self._received_q.empty():
            self._received += self._received_q.get()
        return self._received

    def _listen_server(self, range_dir, output, queue, done):
        country_lookup = Country_Lookup()
        country_lookup.add_range_dir(range_dir)
        hp = Helper_Class()
        queue.put("ready")
        while True:
            try:
                for ip, port in self._receive.yield_synack(10):
                    result = hp.scan_port(ip, port)
                    if result:
                        result['country'] = country_lookup.find(ip)
                        output.write("%s\n" % result)
                        output.flush()
                        queue.put(1)
            except TimeoutError: # only exit if wait or is_alive is called
                print "timeout"
                if not done.empty():
                    print "done"
                    output.close()
                    return

    def listen(self, range_dir, output):
        self.listen_server = multiprocessing.Process(
            target=self._listen_server,
            args=(range_dir, output, self._received_q, self._done))
        self.listen_server.daemon = True
        self.listen_server.start()
        self._received_q.get()
        print "\033[92m[+]\033[1;m Listening"

    def wait(self, timeout=None):
        self._done.put("done")
        self.listen_server.join()
        self.__del__()

    def is_alive(self):
        self._done.put("done")
        return self.listen_server.is_alive()

    def __del__(self):
        try:self.listen_server.terminate()
        except:pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("range_dir", help="range directory")
    parser.add_argument("output", help="output file for results")
    args = parser.parse_args()
    ls = Listen_Server()
    ls.listen(args.range_dir, args.output)
    ls.wait()
