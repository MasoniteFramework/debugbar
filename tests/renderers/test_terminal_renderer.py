import unittest
from src.debugbar.debugger import Debugger
from src.debugbar.collectors.PythonCollector import PythonCollector
from src.debugbar.collectors.MessageCollector import MessageCollector
from src.debugbar.collectors.LogCollector import LogCollector
from src.debugbar.renderers.TerminalRenderer import TerminalRenderer
import logging


class TestPythonCollector(unittest.TestCase):

    def test_can_add_messages(self):
        debugger = Debugger()
        debugger.add_collector(PythonCollector())
        debugger.add_collector(MessageCollector())
        debugger.add_collector(LogCollector())
        debugger.get_collector('messages').add_message("Test", "Testing")
        debugger.get_collector('logging').start_logging("package.logging")

        debugger.get_collector('logging').start_logging("package.log")

        log = logging.getLogger('package.log')
        log.setLevel(logging.DEBUG)
        log.info(f"select * from `users` where `active` = '1'", extra={"time": 100})

        renderer = TerminalRenderer(debugger)
        renderer.render()
