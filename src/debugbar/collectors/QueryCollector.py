import logging
from jinja2.environment import Template

from ..messages.Message import Message


class QueryCollector:
    def __init__(self, name="Queries"):
        self.messages = []
        self.name = name

    def add_message(self, message, subject=None, options=None):
        self.messages.append(Message(subject, message, options=options))
        return self

    def restart(self):
        self.messages = []
        return self

    def start_logging(self, log):
        logger = logging.getLogger(log)
        logger.setLevel(logging.DEBUG)

        logger.addHandler(LogHandler(self))
        return self

    def collect(self):
        collection = []
        queries = []
        duplicated = 0
        total_time = 0
        for message in self.messages:
            query = message.options.get("query")
            bindings = message.options.get("bindings")
            color = "black"
            tags = []

            if bindings:
                for bind in bindings:
                    query = query.replace("%s", bind, 1)

            tags.append(
                {
                    "message": message.options.get("time", ""),
                    "color": "green",
                }
            )
            total_time += float(message.options.get("query_time", 0))
            if float(message.options.get("query_time", 0)) >= 10:
                tags.append(
                    {
                        "message": "Slow",
                        "color": "yellow",
                    }
                )

            if query in queries:
                tags.append(
                    {
                        "message": "Duplicated",
                        "color": "red",
                    }
                )
                color = "red"
                duplicated += 1

            queries.append(query)

            collection.append(
                {
                    "query": query,
                    "color": color,
                    "time": message.options.get("time"),
                    "tags": tags,
                }
            )
        template = Template(self.html())
        return {
            "description": f"{duplicated} duplicated, {len(collection) - duplicated} unique and {len(collection)} total queries in {total_time}ms",
            "count": len(collection),
            "data": collection,
            "html": template.render({"data": collection}),
        }

    def html(self):
        return """
        {% for object in data %}
            <div class="flex justify-between px-4 alternate-gray alternate-white">
                <p class="place-items-center grid py-4 text-{{ object.color }}-700">{{ object.query }}</p>
                <div>
                    {% for tag in object.tags %}
                        <div class="text-right">
                        <span class="inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white rounded bg-{{ tag.color }}-700">{{ tag.message }}</span>
                        </div>
                    {% endfor %}
                </div>
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
                "time": f"{log.query_time}ms",
                "query_time": log.query_time,
                "query": log.query,
                "bindings": log.bindings,
                "level": log.levelname,
            },
        )
