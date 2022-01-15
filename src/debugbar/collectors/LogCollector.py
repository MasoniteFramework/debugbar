import logging
from jinja2 import Template

from ..messages.Message import Message


class LogCollector:
    def __init__(self):
        self.messages = []
        self.name = "logging"

    def add_message(self, message, subject=None, options=None):
        self.messages.append(Message(subject, message, options=options))
        return self

    def start_logging(self, log):
        logger = logging.getLogger(log)

        logger.addHandler(LogHandler(self))
        return self

    def collect(self):
        collection = []
        info_colors = {
            "INFO": "green",
            "DEBUG": "gray",
            "": "black",
        }
        for message in self.messages:
            collection.append(
                {
                    "subject": message.name,
                    "message": message.value,
                    "tags": [
                        {
                            "message": message.options.get("level", ""),
                            "color": info_colors[message.options.get("level", "")],
                        }
                    ],
                }
            )
        template = Template(self.html())
        return {
            "description": "Logging",
            "data": collection,
            "html": template.render({"data": collection}),
        }

    def html(self):
        return """
        {% for object in data %}
            <div class="flex justify-between px-4 alternate-gray alternate-white">
                <div>
                    <span>{{ object.subject }}</span>
                    <span>{{ object.message }}</span>
                </div>
                {% for tag in object.tags %}
                    <div>
                        <span class="inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white rounded" class="bg-{{ tag.color }}-700">{{ tag.message }}</span>
                    </div>
                {% endfor %}
            </div>
        {% endfor %}
        """


class LogHandler(logging.Handler):
    def __init__(self, collector, level=logging.NOTSET):
        super().__init__(level)
        self.collector = collector

    def handle(self, log):
        self.collector.add_message(
            log.msg,
            log.name,
            options={
                "file": log.filename,
                # "time": f"{log.query_time}ms",
                "lineno": log.lineno,
                "logger_name": log.name,
                "level": log.levelname,
            },
        )
