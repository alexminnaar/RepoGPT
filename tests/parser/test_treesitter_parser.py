import unittest
from repogpt.parsers.java_treesitter_parser import JavaTreeSitterParser
from repogpt.parsers.cpp_treesitter_parser import CppTreeSitterParser
from repogpt.parsers.go_treesitter_parser import GoTreeSitterParser
from repogpt.parsers.js_treesitter_parser import JsTreeSitterParser
import os


class TreeSitterParserTest(unittest.TestCase):
    def test_treesitter_parser_java_file(self):
        test_dir = os.path.dirname(os.path.abspath(__file__))
        relative_path = "test_code_files/test_java_file.java"
        file_path = os.path.join(test_dir, relative_path)

        with open(file_path, 'r') as file:
            file_contents = file.read()

        tsp = JavaTreeSitterParser()
        fs = tsp.get_file_summary(file_contents, "test.java")

        actual_methods = [(m.name, m.start_line, m.end_line) for m in fs.methods]
        actual_classes = [(c.name, c.start_line, c.end_line) for c in fs.classes]

        expected_methods =[('RectangleClass', 5, 8), ('calculateArea', 10, 12),
                           ('calculatePerimeter', 14, 16), ('Square', 23, 25),
                           ('createSquare', 27, 29), ('CircleStatic', 36, 38),
                           ('calculateArea', 40, 42), ('calculateCircumference', 44, 46),
                           ('CircleInstance', 53, 55), ('calculateArea', 57, 59),
                           ('calculateCircumference', 61, 63), ('main', 67, 79)]
        expected_classes = [('RectangleClass', 1, 17), ('Square', 20, 30), ('CircleStatic', 33, 47),
                            ('CircleInstance', 50, 64), ('Main', 66, 80)]

        assert actual_methods == expected_methods and actual_classes == expected_classes

    def test_treesitter_parser_cpp_file(self):
        test_dir = os.path.dirname(os.path.abspath(__file__))
        relative_path = "test_code_files/test_cpp_file.cpp"
        file_path = os.path.join(test_dir, relative_path)

        with open(file_path, 'r') as file:
            file_contents = file.read()

        tsp = CppTreeSitterParser()
        fs = tsp.get_file_summary(file_contents, "test.cpp")

        actual_methods = [(m.name, m.start_line, m.end_line) for m in fs.methods]
        actual_classes = [(c.name, c.start_line, c.end_line) for c in fs.classes]

        expected_methods = [('RectangleClass', 10, 10), ('calculateArea', 12, 12),
                            ('calculatePerimeter', 16, 16), ('Square', 27, 27),
                            ('createSquare', 29, 29), ('calculateSquareArea', 34, 34),
                            ('calculateSquarePerimeter', 38, 38), ('CircleStatic', 48, 48),
                            ('calculateArea', 50, 50), ('calculateCircumference', 54, 54),
                            ('CircleInstance', 65, 65), ('calculateArea', 67, 67),
                            ('calculateCircumference', 71, 71), ('main', 76, 76)]
        expected_classes = [('RectangleClass', 4, 19), ('Square', 22, 32), ('CircleStatic', 43, 57),
                            ('CircleInstance', 60, 74)]

        assert actual_methods == expected_methods and actual_classes == expected_classes

    def test_treesitter_parser_js_file(self):
        test_dir = os.path.dirname(os.path.abspath(__file__))
        relative_path = "test_code_files/test_js_file.js"
        file_path = os.path.join(test_dir, relative_path)

        with open(file_path, 'r') as file:
            file_contents = file.read()

        tsp = JsTreeSitterParser()
        fs = tsp.get_file_summary(file_contents, "test.js")

        actual_methods = [(m.name, m.start_line, m.end_line) for m in fs.methods]
        actual_classes = [(c.name, c.start_line, c.end_line) for c in fs.classes]

        expected_methods = [('constructor', 2, 2), ('calculateArea', 7, 7),
                            ('calculatePerimeter', 11, 11)]
        expected_classes = [('Rectangle', 1, 14)]

        assert actual_methods == expected_methods and actual_classes == expected_classes

    def test_treesitter_parser_go_file(self):
        test_dir = os.path.dirname(os.path.abspath(__file__))
        relative_path = "test_code_files/test_go_file.go"
        file_path = os.path.join(test_dir, relative_path)

        with open(file_path, 'r') as file:
            file_contents = file.read()

        tsp = GoTreeSitterParser()
        fs = tsp.get_file_summary(file_contents, "test.go")

        actual_methods = [(m.name, m.start_line, m.end_line) for m in fs.methods]
        actual_classes = [(c.name, c.start_line, c.end_line) for c in fs.classes]

        expected_methods = [('FullName', 14, 16), ('PrintEmployeeInfo', 29, 32), ('main', 34, 48)]
        expected_classes = [('Person', 7, 11), ('Shape', 18, 20), ('Employee', 23, 26)]

        assert actual_methods == expected_methods and actual_classes == expected_classes
