import unittest
from src.debugbar.debugger import Debugger
from src.debugbar.collectors.MessageCollector import MessageCollector

class TestMessageCollector(unittest.TestCase):

    def test_can_add_messages(self):
        debugger = Debugger()
        debugger.add_collector(MessageCollector())

        debugger.get_collector('Messages').add_message("foobar")
        self.assertTrue(len(debugger.get_collector('Messages').messages) == 1)
