from masonite.providers import Provider
from ..Debugger import Debugger
from ..collectors.MessageCollector import MessageCollector
from ..collectors.PythonCollector import PythonCollector
from ..collectors.QueryCollector import QueryCollector
from ..collectors.KeyValueCollector import KeyValueCollector
from ..collectors.MeasureCollector import MeasureCollector
# from masonite.facades import Cache
from masonite.utils.str import random_string  
import json
import time
import glob
import os

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
        debugger.add_collector(KeyValueCollector("Request"))
        debugger.add_collector(QueryCollector().start_logging('masoniteorm.connection.queries'))
        self.application.bind('debugger', debugger)

    def boot(self):
        self.application.make('debugger').get_collector('Time').stop_measure('boot')
        response = self.application.make('response')
        storage = self.application.make('storage')
        if 'text/html' in response.header('Content-Type'):
            # Delete the contents of the directory first
            files = glob.glob('storage/app/debug/*')
            for f in files:
                os.remove(f)

            storage.disk('debug').put(f"x{str(time.time())+'-'+random_string(10)}.json", json.dumps(self.application.make('debugger').to_dict()))
            response.content += self.application.make('debugger').get_renderer('javascript').render()
            response.make_headers()
        else:
            storage.disk('debug').put(f"x{str(time.time())+'-'+random_string(10)}.json", json.dumps(self.application.make('debugger').to_dict()))
