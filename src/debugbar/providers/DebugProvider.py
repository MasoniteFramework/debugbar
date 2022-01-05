from masonite.providers import Provider
from ..debugger import Debugger
from ..collectors.MessageCollector import MessageCollector
from ..collectors.PythonCollector import PythonCollector
from ..collectors.QueryCollector import QueryCollector
from ..collectors.KeyValueCollector import KeyValueCollector
from ..collectors.MeasureCollector import MeasureCollector


class DebugProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        debugger = Debugger()
        time = MeasureCollector("Time")
        time.start_measure('boot')
        debugger.add_collector(MessageCollector())
        debugger.add_collector(KeyValueCollector("Environment"))
        debugger.add_collector(time)
        # debugger.add_collector(KeyValueCollector("Request"))
        debugger.add_collector(QueryCollector().start_logging('masoniteorm.connection.queries'))
        self.application.bind('debugger', debugger)

    def boot(self):
        self.application.make('debugger').get_collector('Time').stop_measure('boot')
        response = self.application.make('response')
        if 'text/html' in response.header('Content-Type'):
            response.content += bytes(self.application.make('debugger').get_renderer('javascript').render(), "utf-8")
            response.make_headers()
