
class Debugger:

    def __init__(self):
        self.collectors = {}

    def add_collector(self, collector):
        self.collectors.update({collector.name: collector})
        return self

    def get_collector(self, name):
        return self.collectors[name]



