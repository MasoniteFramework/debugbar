import unittest
from src.debugbar.Debugger import Debugger
from src.debugbar.collectors.MessageCollector import MessageCollector

class TestMessageCollector(unittest.TestCase):

    def test_can_add_messages(self):
        debugger = Debugger()
        debugger.add_collector(MessageCollector())

        debugger.get_collector('messages').add_message("foobar")
        self.assertTrue(len(debugger.get_collector('messages').messages) == 1)
