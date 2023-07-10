from repogpt.parsers.base import Parser
from pygments.lexers import get_lexer_by_name
from pygments.token import Token
from typing import List



class JavaParser(Parser):
    @staticmethod
    def get_file_summary(code: str, file_name: str = None) -> List[str]:
        lexer = get_lexer_by_name('java')
        tokens = lexer.get_tokens(code)

        classes_and_methods = []

        line = 1
        for token_type, token_value in tokens:
            if token_type == Token.Name.Function:
                classes_and_methods.append(f"Method named {token_value} starting on line {line}")
            elif token_type == Token.Name.Class:
                classes_and_methods.append(f"Class named {token_value} starting on line {line}")
            elif token_value == "\n":
                line += 1

        return classes_and_methods
