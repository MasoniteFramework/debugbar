from ..messages.Message import Message
import logging

class QueryCollector:

    def __init__(self):
        self.messages = []
        self.name = "query"

    def add_message(self, message, subject=None, options=None):
        print('rr', options)
        self.messages.append(Message(subject, message, options=options))
        return self

    def start_logging(self, log):
        logger = logging.getLogger(log)
        
        logger.addHandler(LogHandler(self))
        return self

    def collect(self):
        collection = []
        queries = []
        duplicated = 0
        total_time = 0
        for message in self.messages:
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
                # 'subject': message.subject,
                'message': query,
                'color': color,
                'tags': tags,
            })

        return {
            'description': f"{duplicated} duplicated, {len(collection) - duplicated} unique and {len(collection)} total queries in {total_time}ms",
            'data': collection,   
        }

class LogHandler(logging.Handler):

    def __init__(self, collector, level=logging.NOTSET):
        super().__init__(level)
        self.collector = collector

    def handle(self, log):
        print('handling log')
        self.collector.add_message(log.msg, log.name, options={
            "time": f"{log.query_time}ms",
            "query_time": log.query_time,
            "query": log.query,
            "bindings": log.bindings,
            "level": log.levelname,
        })