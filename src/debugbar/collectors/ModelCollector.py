from ..messages.Message import Message
import logging

class ModelCollector:

    def __init__(self, name="models"):
        self.models = {}
        self.name = name

    def restart(self):
        self.models = {}
        return self

    def start_logging(self, log):
        logger = logging.getLogger(log)
        logger.propagate = True
        logger.setLevel(logging.DEBUG)


        logger.addHandler(ModelHandler(self))
        return self

    def collect(self):
        collection = []
        total_count = 0
        for model, count in self.models.items():
            collection.append({
                "id": model,
                'class_name': model,
                'count': count,
            })
            total_count += count



        return {
            'description': "Models",
            'count': total_count,
            'data': collection,
            'html': self.html(),
        }

    def html(self):
        return """
        <template x-for="object in currentContent.data" :key="object.id">
            <div class="flex flex-1 odd:bg-gray-100 p-4">
                <div class="pr-4" x-text="object.class_name"></div>
                <div x-text="object.count"></div>
            </div>
        </template>"""

class ModelHandler(logging.Handler):

    def __init__(self, collector, level=logging.NOTSET):
        super().__init__(level)
        self.collector = collector

    def handle(self, log):
        full_path = f"{log.class_module}.{log.class_name}"
        if not full_path in self.collector.models:
            self.collector.models[full_path] = 1
        else:
            self.collector.models[full_path] += 1