from repogpt.parsers.base import Parser
from pygments.lexers import get_lexer_for_filename
from pygments.token import Token
from typing import List


class PygmentsParser(Parser):

    @staticmethod
    def get_file_summary(code: str, file_name: str = None) -> List[str]:
        lexer = get_lexer_for_filename(file_name)
        tokens = lexer.get_tokens(code)

        classes_and_methods = []

        line = 1
        for token_type, token_value in tokens:
            if token_type == Token.Name.Function:
                classes_and_methods.append(f"method named {token_value} starting on line {line}")
            elif token_type == Token.Name.Class:
                classes_and_methods.append(f"class named {token_value} starting on line {line}")
            if token_value == "\n" or token_type == Token.Name.Whitespace:
                line += 1
            if token_type == Token.Literal.String.Doc:
                line += token_value.count('\n')

        return classes_and_methods
