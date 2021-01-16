import unittest
from src.debugbar.debugger import Debugger
from src.debugbar.collectors.PythonCollector import PythonCollector
from platform import python_version


class TestPythonCollector(unittest.TestCase):

    def test_can_add_messages(self):
        debugger = Debugger()
        debugger.add_collector(PythonCollector())

        collection = debugger.get_collector('python').collect()
        self.assertEqual(collection, {'python': {'version': python_version()}})
