import time
from jinja2 import Template

from ..messages.Measure import Measure


class MeasureCollector:
    def __init__(self, name=""):
        self.measures = {}
        self.name = name

    def restart(self):
        return self

    def start_measure(self, key, value=None):
        self.measures.update({key: Measure(value or time.time())})
        return self

    def stop_measure(self, key):
        self.measures.get(key).stop_measure(time.time())
        return self

    def collect(self):
        collection = []
        for key, measure in self.measures.items():
            collection.append(
                {
                    "name": key,
                    "start": measure.start_time,
                    "stop": measure.stop_time,
                    "diff": measure.diff,
                }
            )
        template = Template(self.html())
        return {
            "description": "Time Measurements in seconds",
            "count": len(collection),
            "data": collection,
            "html": template.render({"data": collection}),
        }

    def html(self):
        return """
        {% for object in data %}
            <div class="flex flex-1 alternate-gray alternate-white p-4">
                <div class="pr-4">{{ object.name }}</div>
                <div>{{ object.diff }}</div>
            </div>
        {% endfor %}"""
