from ..messages.Message import Message
import logging

class QueryCollector:

    def __init__(self):
        self.messages = []
        self.name = "query"

    def add_message(self, message, subject=None, options=None):
        self.messages.append(Message(subject, message, options=options))
        return self

    def start_logging(self, log):
        logger = logging.getLogger(log)
        logger.setLevel(10)

        logger.addHandler(LogHandler(self))
        return self

    def collect(self):
        collection = []
        queries = []
        duplicated = 0
        total_time = 0
        for index, message in enumerate(self.messages):
            query = message.options.get("query")
            color = "black"
            tags = []

            tags.append({
                'message': message.options.get('time', ''),
                'color': 'green',
            })
            total_time += float(message.options.get('query_time', 0))
            if float(message.options.get('query_time', 0)) >= 10:
                tags.append({
                    'message': 'Slow',
                    'color': 'yellow',
                })

            if query in queries:
                tags.append({
                    'message': 'Duplicated',
                    'color': 'red',
                })
                color = "red"
                duplicated += 1

            queries.append(query)


            collection.append({
                "id": f"{index}_{self.name}",
                'query': query,
                'color': color,
                'time': message.options.get("time"),
                'tags': tags,
            })

        return {
            'description': f"{duplicated} duplicated, {len(collection) - duplicated} unique and {len(collection)} total queries in {total_time}ms",
            'data': collection,
            'html': self.html(),
        }

    def html(self):
        return """
        <template x-for="object in currentContent.data" :key="object.id">
            <div class="flex justify-between px-4 odd:bg-gray-200 even:bg-white">
                <div class="place-items-center grid py-4" x-text="object.query" :class="'text-'+object.color+'-700'"></div>
                <div>
                    <template x-for="tag in object.tags">
                        <div class="text-right">
                        <span class="inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white rounded" :class="'bg-'+tag.color+'-700'" x-text="tag.message"></span>
                        </div>
                    </template>
                </div>
            </div>
        </template>
        """

class LogHandler(logging.Handler):

    def __init__(self, collector, level=logging.NOTSET):
        super().__init__(level)
        self.collector = collector

    def handle(self, log):

        print('query logged')
        self.collector.add_message(log.msg, log.name, options={
            "time": f"{log.query_time}ms",
            "query_time": log.query_time,
            "query": log.query,
            "bindings": log.bindings,
            "level": log.levelname,
        })