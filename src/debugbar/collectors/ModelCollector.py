import logging
from jinja2 import Template


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
            collection.append(
                {
                    "id": model,
                    "class_name": model,
                    "count": count,
                }
            )
            total_count += count

        template = Template(self.html())
        return {
            "description": "Models",
            "count": total_count,
            "data": collection,
            "html": template.render({"data": collection}),
        }

    def html(self):
        return """
        {% for object in data %}
            <div class="flex flex-1 alternate-gray alternate-white p-4">
                <div class="pr-4">{{ object.class_name }}</div>
                <div>{{ object.count }}</div>
            </div>
        {% endfor %}"""


class ModelHandler(logging.Handler):
    def __init__(self, collector, level=logging.NOTSET):
        super().__init__(level)
        self.collector = collector

    def handle(self, log):
        full_path = f"{log.class_module}.{log.class_name}"
        if full_path not in self.collector.models:
            self.collector.models[full_path] = 1
        else:
            self.collector.models[full_path] += 1
