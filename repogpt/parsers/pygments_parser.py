from pygments.lexers import get_lexer_for_filename
from pygments.token import Token
from repogpt.parsers.base import CodeParser, FileSummary, SummaryPosition
from typing import List, Tuple


class PygmentsParser(CodeParser):

    @staticmethod
    def get_summary_from_position(summary_positions: List[SummaryPosition], start_line: int,
                                  end_line: int) -> Tuple[List[str], List[str]]:
        """For a given list of summary positions and start/end lines find which positions are before and inside the lines"""
        last_obj = []
        current_obj = []

        # TODO: binary search-ify this
        for s_pos in summary_positions:
            # get last defined obj before the snippet
            if s_pos.start_line < start_line:
                last_obj.append(s_pos.name)

            # get any obj defined in this snippet
            if start_line <= s_pos.start_line <= end_line:
                current_obj.append(s_pos.name)

            # ignore everything past this snippet
            if s_pos.start_line > end_line:
                break

        return last_obj, current_obj

    @staticmethod
    def get_closest_method_class_in_snippet(file_summary: FileSummary, snippet_start_line: int,
                                            snippet_end_line: int) -> str:
        """For a given file summary and snippet start/end lines extract summary information for the snippet"""

        closest_method_class_summary = ""

        last_class, current_class = PygmentsParser.get_summary_from_position(file_summary.classes, snippet_start_line,
                                                                             snippet_end_line)

        if len(last_class) == 1:
            closest_method_class_summary += f"  The last class defined before this snippet was called {last_class[0]}."
        elif len(last_class) > 1:
            multi_class_summary = " and ".join([f"{c}" for c in last_class])
            closest_method_class_summary += f"  The classes defined before this snippet are {multi_class_summary}."
        if len(current_class) == 1:
            closest_method_class_summary += f"  The class defined in this snippet is called {current_class[0]}."
        elif len(current_class) > 1:
            multi_class_summary = " and ".join([f"{c}" for c in current_class])
            closest_method_class_summary += f"  The classes defined in this snippet are {multi_class_summary}."

        last_method, current_method = PygmentsParser.get_summary_from_position(file_summary.methods, snippet_start_line,
                                                                     snippet_end_line)

        if last_method:
            closest_method_class_summary += f"  The beginning of this snippet contains the end of the {last_method[-1]} " \
                                            "method."
        if len(current_method) == 1:
            closest_method_class_summary += f"  The method defined in this snippet is called {current_method[0]}."
        elif len(current_method) > 1:
            multi_method_summary = " and ".join([f"{meth}" for meth in current_method])
            closest_method_class_summary += f"  The methods defined in this snippet are {multi_method_summary}."

        return closest_method_class_summary

    @staticmethod
    def get_file_summary(code: str, file_name: str) -> FileSummary:
        """Use the Pygments parser to extract summary of file's methods and classes and their starting lines"""
        lexer = get_lexer_for_filename(file_name)
        tokens = lexer.get_tokens(code)

        file_summary = FileSummary()

        line = 1
        for token_type, token_value in tokens:
            # extract name and line of method in code
            if token_type == Token.Name.Function or token_type == Token.Name.Function.Magic:
                file_summary.add_method(token_value, line)
            # extract name and line of class in code
            elif token_type == Token.Name.Class:
                file_summary.add_class(token_value, line)
            if token_value == "\n" or token_type == Token.Name.Whitespace:
                line += 1
            if token_type == Token.Literal.String.Doc:
                line += token_value.count('\n')

        return file_summary
