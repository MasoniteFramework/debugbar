from logging import debug
from masonite.providers import Provider
from masonite.packages import PackageProvider
from ..debugger import Debugger
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
from masonite.routes import Route
from ..controllers.DebugController import DebugController
from masonite.utils.location import base_path
import json
import time
import glob
import os
import timeit


class DebugProvider(PackageProvider):
    def configure(self):
        (
            self.root("debugbar")
            .name("debugbar")
            .config("scaffold/debug.py", publish=True)
        )

    def register(self):
        super().register()
        debugger = Debugger()
        self.application.make("storage").store_config.update(
            {
                "debug": {"driver": "file", "path": base_path("storage/app/debug")},
            }
        )

        options = config("debugbar.options")

        if options.get("messages"):
            debugger.add_collector(MessageCollector())

        if options.get("environment"):
            debugger.add_collector(KeyValueCollector("Environment", "Environment Related Fields"))

        if options.get("models"):
            debugger.add_collector(
                ModelCollector("Models").start_logging("masoniteorm.models.hydrate")
            )

        if options.get("queries"):
            debugger.add_collector(
                QueryCollector().start_logging("masoniteorm.connection.queries")
            )

        if options.get("measures"):
            debugger.add_collector(MeasureCollector("Measures"))

        if options.get("request"):
            debugger.add_collector(KeyValueCollector("Request", "Request Information"))

        self.application.bind("debugger", debugger)
        self.application.make("router").add(
            Route.group(
                [
                    Route.get("/_debugbar/@id", DebugController.get_debug),
                    Route.get("/_debugbar/", DebugController.debug),
                ]
            )
        )

    def boot(self):
        debugger = self.application.make("debugger")
        response = self.application.make("response")
        storage = self.application.make("storage")
        options = config("debugbar.options")
        if options.get("environment"):
            debugger.get_collector("Environment").add(
                "Python Version", python_version()
            )
            from masonite import __version__
            debugger.get_collector("Environment").add(
                "Masonite Version", __version__
            )
        if options.get("measures"):
            debugger.get_collector("Measures").start_measure("Application Time", self.application.make("start_time"))
            debugger.get_collector("Measures").stop_measure("Application Time")

        request_id = str(time.time()) + "-" + random_string(10)

        if "text/" in response.header("Content-Type"):
            for f in glob.glob("storage/app/debug/*"):
                os.remove(f)
            response.content += (
                self.application.make("debugger").get_renderer("javascript").render()
            )
            response.make_headers()

        else:
            request_id = f"x{request_id}"
        if options.get("request"):
            debugger.get_collector("Request").add(
                "Input", self.application.make("request").all()
            )
            debugger.get_collector("Request").add(
                "Request Parameters", self.application.make("request").params
            )
            debugger.get_collector("Request").add(
                "Request Headers", self.application.make("request").header_bag.to_dict()
            )
            debugger.get_collector("Request").add(
                "Response Headers", self.application.make("response").header_bag.to_dict()
            )

        debug_info = {
            "__meta": {
                "request_url": self.application.make("request").get_path(),
                "request_id": request_id,
            }
        }
        debug_info.update({"data": debugger.to_dict()})
        if "_debugbar" not in self.application.make("request").get_path():
            storage.disk("debug").put(f"{request_id}.json", json.dumps(debug_info))

        debugger.restart_collectors()
