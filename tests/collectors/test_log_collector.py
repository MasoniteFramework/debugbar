import unittest
from src.debugbar.debugger import Debugger
from src.debugbar.collectors.LogCollector import LogCollector
import logging


class TestLogCollector(unittest.TestCase):
    def test_can_add_messages(self):
        debugger = Debugger()
        debugger.add_collector(LogCollector())

        debugger.get_collector("logging").start_logging("package.log")

        log = logging.getLogger("package.log")
        log.setLevel(logging.DEBUG)
        log.info("here")
