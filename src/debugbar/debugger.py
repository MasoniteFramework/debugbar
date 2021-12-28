import json

class Debugger:

    def __init__(self):
        self.collectors = {}

    def add_collector(self, collector):
        self.collectors.update({collector.name: collector})
        return self

    def get_collector(self, name):
        return self.collectors[name]

    def to_json(self):
        renderer = {}
        for key, collector in self.collectors.items():
            renderer.update({key: collector.collect()})

        return json.dumps(renderer)

    def to_dict(self):
        renderer = {}
        for key, collector in self.collectors.items():
            renderer.update({key: collector.collect()})

        return renderer

