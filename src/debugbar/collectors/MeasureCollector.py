from ..messages.Measure import Measure
from platform import python_version
import timeit

class MeasureCollector:

    def __init__(self, name=""):
        self.measures = {}
        self.name = name

    def start_measure(self, key):
        self.measures.update({key: Measure(timeit.timeit())})
        return self

    def stop_measure(self, key):
        self.measures.get(key).stop_measure(timeit.timeit())
        return self

    def collect(self):
        collection = []
        for key, measure in self.measures.items():
            collection.append({
                "name": key, 
                "start": measure.start_time, 
                "stop": measure.stop_time,
                "diff": measure.diff,
                "html": """
                    <template x-for="(object, index) in currentContent">
                        <div class="flex flex-1 odd:bg-gray-100">
                            <div class="pr-4" x-text="object.name"></div>
                            <div x-text="object.diff"></div>
                        </div>
                    </template>
                """
            }
        )

        return {
            'description': "Python Version",
            'data': collection,   
        }