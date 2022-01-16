class Measure:
    def __init__(self, start_time, stop_time=None):
        self.start_time = start_time
        self.stop_time = stop_time
        self.diff = None

    def start_measure(self, start):
        self.start_time = start
        return self

    def stop_measure(self, stop):
        self.stop_time = stop
        self.diff = self.stop_time - self.start_time
        self.diff = f"{self.diff:.2f}s"
        return self
