class JavascriptDebugRenderer:

    def __init__(self, debugger):
        self.debugger = debugger

    def render(self, meta=None):
        data = {}
        if meta is None:
            meta = []
        for name, collector in self.debugger.collectors.items():
            data.update({collector.name: collector.collect()})
        return {
            "meta": meta,
            "data": data,
        }