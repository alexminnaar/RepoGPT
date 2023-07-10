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
        expected_python_summary = ['method named my_function starting on line 1',
                                   'class named MyClass starting on line 5',
                                   'method named my_method starting on line 6']

        test_python_summary = PygmentsParser.get_file_summary(test_python_code, "test_python_file.py")

        assert test_python_summary == expected_python_summary

    def test_pygments_parser_cpp(self):
        test_cpp_code = """
        #include <iostream>

        void myFunction() {
            // Function body goes here
        }

        class MyClass {
        void myMethod() {
                // Method body goes here
            }
        };
        """
        expected_cpp_summary = ['method named myFunction starting on line 3',
                                'class named MyClass starting on line 6',
                                'method named myMethod starting on line 7']

        test_cpp_summary = PygmentsParser.get_file_summary(test_cpp_code, "test_cpp_file.cpp")

        assert test_cpp_summary == expected_cpp_summary

    def test_pygments_parser_java(self):
        test_java_code = """
        public class MyClass {
            public void myMethod() {
                // Method body goes here
            }

            private int calculateSum(int a, int b) {
                // Method body goes here
                return a + b;
            }
        }
        """
        expected_java_summary = ["class named MyClass starting on line 1",
                                 "method named myMethod starting on line 2",
                                 "method named calculateSum starting on line 6"]
        test_java_summary = PygmentsParser.get_file_summary(test_java_code, "test_java_file.java")

        assert test_java_summary == expected_java_summary
