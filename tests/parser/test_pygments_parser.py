import unittest
from repogpt.parsers.pygments_parser import PygmentsParser


class PygmentsParserTest(unittest.TestCase):

    def test_pygments_parser_python(self):
        test_python_code = """
def my_function():
    # Function body goes here
    pass

class MyClass:
    def my_method(self):
        # Method body goes here
        pass
"""

        test_python_summary = PygmentsParser.get_file_summary(test_python_code, "test_python_file.py")

        assert len(test_python_summary.classes) == 1 \
               and test_python_summary.classes[0].name == 'MyClass' \
               and test_python_summary.classes[0].start_line == 5 \
               and len(test_python_summary.methods) == 2 \
               and test_python_summary.methods[0].name == 'my_function' \
               and test_python_summary.methods[0].start_line == 1 \
               and test_python_summary.methods[1].name == 'my_method' \
               and test_python_summary.methods[1].start_line == 6
