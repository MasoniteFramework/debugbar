from tabulate import tabulate


class TerminalRenderer:
    def __init__(self, debugger):
        self.debugger = debugger

    def render(self):
        for name, collector in self.debugger.collectors.items():
            print()
            table = []
            print(collector.name.capitalize(), "Collector")
            for key, value in collector.collect().items():
                table.append([key, value])
            print(tabulate(table))
