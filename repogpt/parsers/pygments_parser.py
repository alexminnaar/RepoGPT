from pygments.lexers import get_lexer_for_filename
from pygments.token import Token
from typing import List, Tuple


class SummaryPosition:
    def __init__(self, name: str, line: int):
        self.name = name
        self.line = line


class FileSummary:
    def __init__(self):
        self.classes = []
        self.methods = []

    def add_class(self, class_name: str, class_line: int):
        self.classes.append(SummaryPosition(class_name, class_line))

    def add_method(self, method_name: str, method_line: int):
        self.methods.append(SummaryPosition(method_name, method_line))


class PygmentsParser:

    @staticmethod
    def get_file_summary(code: str, file_name: str = None) -> FileSummary:
        """Use the Pygments parser to extract summary of file's methods and classes and their starting lines"""
        lexer = get_lexer_for_filename(file_name)
        tokens = lexer.get_tokens(code)

        file_summary = FileSummary()

        line = 1
        for token_type, token_value in tokens:
            # extract name and line of method in code
            if token_type == Token.Name.Function or token_type == Token.Name.Function.Magic:
                file_summary.add_method(token_value, line)
            #extract name and line of class in code
            elif token_type == Token.Name.Class:
                file_summary.add_class(token_value, line)
            if token_value == "\n" or token_type == Token.Name.Whitespace:
                line += 1
            if token_type == Token.Literal.String.Doc:
                line += token_value.count('\n')

        return file_summary
