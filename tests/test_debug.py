import unittest
from src.debugbar.debugger import Debugger
from src.debugbar.collectors.MessageCollector import MessageCollector
from src.debugbar.collectors.PythonCollector import PythonCollector


class TestDebugBar(unittest.TestCase):

    def test_can_add_messages(self):
        debugger = Debugger()
        debugger.add_collector(MessageCollector())
        debugger.add_collector(PythonCollector())

        debugger.get_collector('Messages').add_message("Success")
        debugger.get_collector('Messages').add_message("Failure")

        print(debugger.to_dict())