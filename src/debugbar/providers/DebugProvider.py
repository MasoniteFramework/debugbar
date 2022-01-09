from logging import debug
from masonite.providers import Provider
from ..Debugger import Debugger
from ..collectors.MessageCollector import MessageCollector
from ..collectors.PythonCollector import PythonCollector
from ..collectors.QueryCollector import QueryCollector
from ..collectors.KeyValueCollector import KeyValueCollector
from ..collectors.MeasureCollector import MeasureCollector
from ..collectors.ModelCollector import ModelCollector
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
        debugger.add_collector(ModelCollector("Models").start_logging("masoniteorm.models.hydrate"))
        debugger.add_collector(time)
        debugger.add_collector(KeyValueCollector("Request", "Request Information"))
        debugger.add_collector(QueryCollector().start_logging('masoniteorm.connection.queries'))
        self.application.bind('debugger', debugger)

    def boot(self):
        debugger = self.application.make('debugger')
        debugger.get_collector('Time').stop_measure('boot')
        response = self.application.make('response')
        storage = self.application.make('storage')
        
        request_id = str(time.time())+'-'+random_string(10)

        if 'text/' in response.header('Content-Type'):
            # Delete the contents of the directory first
            files = glob.glob('storage/app/debug/*')
            for f in files:
                os.remove(f)
            response.content += self.application.make('debugger').get_renderer('javascript').render()
            response.make_headers()
            
        else:
            request_id = f"x{request_id}"
        
        debugger.get_collector('Request').add('input', self.application.make('request').all())
        debugger.get_collector('Request').add('headers', self.application.make('request').header_bag.to_dict())
        debug_info = {
            "__meta": {
                "request_url": self.application.make('request').get_path(),
                "request_id": request_id
            }
        }
        debug_info.update({"data": self.application.make('debugger').to_dict()})
        if "_debugbar" not in self.application.make('request').get_path():
            storage.disk('debug').put(f"{request_id}.json", json.dumps(debug_info))
        
        debugger.restart_collectors()
