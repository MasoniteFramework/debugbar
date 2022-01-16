import json
from .renderers.JavascriptDebugRenderer import JavascriptDebugRenderer


class Debugger:
    def __init__(self):
        self.collectors = {}
        self.renderers = {
            "javascript": JavascriptDebugRenderer,
        }

    def add_renderer(self, name, renderer):
        self.renderers.update({name: renderer})
        return self

    def get_renderer(self, name):
        return self.renderers[name](self)

    def add_collector(self, collector):
        self.collectors.update({collector.name.capitalize(): collector})
        return self

    def get_collector(self, name):
        return self.collectors[name.capitalize()]

    def restart_collector(self, name):
        return self.collectors[name].restart()

    def restart_collectors(self):
        for name, collector in self.collectors.items():
            collector.restart()

        return self

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
