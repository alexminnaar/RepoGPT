from repogpt.parsers.base import CodeParser, FileSummary, SummaryPosition
import ast
from typing import List, Tuple


class PythonParser(CodeParser):
    @staticmethod
    def get_summary_from_position(summary_positions: List[SummaryPosition], start_line: int,
                                  end_line: int) -> Tuple[List[SummaryPosition], List[SummaryPosition]]:

        last_obj = []
        current_obj = []

        # TODO: binary search-ify this
        for s_pos in summary_positions:
            # get last defined method before the snippet
            if s_pos.start_line < start_line and s_pos.end_line >= start_line:
                last_obj.append(s_pos)

            # get any method defined in this snippet
            if start_line <= s_pos.start_line <= end_line:
                current_obj.append(s_pos)

            # ignore everything past this snippet
            if s_pos.start_line > end_line:
                break
        return last_obj, current_obj

    @staticmethod
    def get_closest_method_class_in_snippet(file_summary: FileSummary, snippet_start_line: int,
                                            snippet_end_line: int) -> str:
        closest_method_class_summary = ""

        last_class, current_class = PythonParser.get_summary_from_position(file_summary.classes, snippet_start_line,
                                                                           snippet_end_line)

        if last_class:
            closest_method_class_summary += f"  The last class defined before this snippet was called `{last_class[-1].name}` " \
                                            f"starting at line {last_class[-1].start_line} and ending at line {last_class[-1].end_line}."
        if len(current_class) == 1:
            closest_method_class_summary += f"  The class defined in this snippet is called `{current_class[0].name}`" \
                                            f"starting at line {current_class[0].start_line} and ending at line {current_class[0].end_line}."
        elif len(current_class) > 1:
            multi_class_summary = " and ".join(
                [f"`{c.name}` starting at line {c.start_line} and ending at line {c.end_line}" for c in current_class])
            closest_method_class_summary += f"  The classes defined in this snippet are {multi_class_summary}."

        last_method, current_method = PythonParser.get_summary_from_position(file_summary.methods, snippet_start_line,
                                                                             snippet_end_line)

        if last_method:
            closest_method_class_summary += f"  The last method starting before this snippet is called `{last_method[-1].name}` " \
                                            f"which starts on line {last_method[-1].start_line} and ends at " \
                                            f"line {last_method[-1].end_line}."
        if len(current_method) == 1:
            closest_method_class_summary += f"  The method defined in this snippet is called `{current_method[0].name}` " \
                                            f"starting at line {current_method[0].start_line} and ending at line " \
                                            f"{current_method[0].end_line}."
        elif len(current_method) > 1:
            multi_method_summary = " and ".join(
                [f"`{meth.name}` starting at line {meth.start_line} and ending at line {meth.end_line}" for meth in
                 current_method])
            closest_method_class_summary += f"  The methods defined in this snippet are {multi_method_summary}."

        return closest_method_class_summary

    @staticmethod
    def get_file_summary(code: str, file_name: str) -> FileSummary:
        """Get the classes and methods in python code.  Here we can get the end lines too."""
        parsed_tree = ast.parse(code)

        file_summary = FileSummary()

        # Traverse the AST to find function and class definitions
        for node in ast.walk(parsed_tree):
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                function_start_line = node.lineno
                function_end_line = node.end_lineno
                file_summary.methods.append(SummaryPosition(function_name, function_start_line, function_end_line))

            elif isinstance(node, ast.ClassDef):
                class_name = node.name
                class_start_line = node.lineno
                class_end_line = node.end_lineno
                file_summary.classes.append(SummaryPosition(class_name, class_start_line, class_end_line))

        # methods and classes are not in order so sort
        file_summary.methods = sorted(file_summary.methods, key=lambda x: x.start_line)
        file_summary.classes = sorted(file_summary.classes, key=lambda x: x.start_line)

        return file_summary
