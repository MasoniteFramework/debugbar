from logging import debug
from masonite.providers import Provider
from masonite.packages import PackageProvider
from ..Debugger import Debugger
from ..collectors.MessageCollector import MessageCollector
from ..collectors.PythonCollector import PythonCollector
from ..collectors.QueryCollector import QueryCollector
from ..collectors.KeyValueCollector import KeyValueCollector
from ..collectors.MeasureCollector import MeasureCollector
from ..collectors.ModelCollector import ModelCollector
# from masonite.facades import Cache
from masonite.configuration import config
from masonite.utils.str import random_string  
from platform import python_version
import json
import time
import glob
import os

class DebugProvider(PackageProvider):
    def configure(self):
        (
            self.root("debugbar")
            .name("debugbar")
        )

    def register(self):
        super().register()
        debugger = Debugger()
        
        options = config('debug.options')

        if options.get("messages"):
            debugger.add_collector(MessageCollector())

        if options.get('environment'):
            debugger.add_collector(KeyValueCollector("Environment"))

        if options.get('models'):
            debugger.add_collector(ModelCollector("Models").start_logging("masoniteorm.models.hydrate"))

        if options.get('measures'):
            debugger.add_collector(MeasureCollector("Time"))

        if options.get('request'):
            debugger.add_collector(KeyValueCollector("Request", "Request Information"))

        if options.get('queries'):
            debugger.add_collector(QueryCollector().start_logging('masoniteorm.connection.queries'))

        self.application.bind('debugger', debugger)

    def boot(self):
        debugger = self.application.make('debugger')
        response = self.application.make('response')
        storage = self.application.make('storage')
        options = config('debug.options')
        if options.get('environment'):
            debugger.get_collector('Environment').add("Python Version", python_version())

        request_id = str(time.time())+'-'+random_string(10)

        if 'text/' in response.header('Content-Type'):
            for f in glob.glob('storage/app/debug/*'):
                os.remove(f)
            response.content += self.application.make('debugger').get_renderer('javascript').render()
            response.make_headers()
            
        else:
            request_id = f"x{request_id}"
        if options.get('request'):
            debugger.get_collector('Request').add('input', self.application.make('request').all())
            debugger.get_collector('Request').add('headers', self.application.make('request').header_bag.to_dict())

        debug_info = {
            "__meta": {
                "request_url": self.application.make('request').get_path(),
                "request_id": request_id
            }
        }
        debug_info.update({"data": debugger.to_dict()})
        if "_debugbar" not in self.application.make('request').get_path():
            storage.disk('debug').put(f"{request_id}.json", json.dumps(debug_info))
        
        debugger.restart_collectors()
