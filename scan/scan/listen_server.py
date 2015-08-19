import time
import inspect
import argparse
import multiprocessing
from scan import banners
from scan.raw_sock import Receive

class Listen_Server:
    def __init__(self):
        self.listen_server = None
        self._receive = Receive()
        self._received_q = multiprocessing.Queue()
        self._received = 0

    @property
    def received(self):
        while not self._received_q.empty():
            self._received += self._received_q.get()
        return self._received

    def _listen_server(self, output, queue):
        banner_modules = {}
        output = open(output, "a")
        classmembers = inspect.getmembers(banners, inspect.isclass)
        for classmember in classmembers:
            if classmember[0] != "Parent" and classmember[0] != "Process":
                cm = classmember[1]()
                banner_modules[int(cm.default_port)] = cm
        for ip, port in self._receive.yield_synack():
            try:
                banner_module = banner_modules[int(port)]
                results = banner_module.run(ip, port)
                if results:
                    output.write("%s\n" % results)
                    output.flush()
                    queue.put(1)
            except:pass

    def listen(self, output):
        self.listen_server = multiprocessing.Process(
            target=self._listen_server,
            args=(output, self._received_q))
        self.listen_server.daemon = True
        self.listen_server.start()
        print "\033[92m[+]\033[1;m Listening"

    def wait(self, timeout=None):
        self.listen_server.join()
        self.__del__()

    def is_alive(self):
        return self.listen_server.is_alive()

    def __del__(self):
        try:self.listen_server.terminate()
        except:pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", help="output file for results")
    args = parser.parse_args()
    ls = Listen_Server()
    ls.listen(args.output)
    ls.wait()
