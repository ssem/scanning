import inspect
import banners


class Helper_Class:
    def __init__(self):
        self.modules = self._get_modules()

    def _get_modules(self):
        banner_modules = {}
        classmembers = inspect.getmembers(banners, inspect.isclass)
        for classmember in classmembers:
            if classmember[0] != "Parent" and classmember[0] != "Process":
                cm = classmember[1]()
                banner_modules[int(cm.default_port)] = cm
        return banner_modules

    def scan_all_ports(self, ip, timeout=.5):
        for module in self.modules:
            result = self.modules[module].run(ip, self.modules[module].default_port, timeout)
            if result != None:
                yield result

    def scan_port(self, ip, port, timeout=.5):
        module = self.modules[int(port)]
        return module.run(ip, port, timeout)
