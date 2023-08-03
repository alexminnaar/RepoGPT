from abc import ABC, abstractmethod
from typing import List, Tuple


class SummaryPosition:
    def __init__(self, name: str, start_line: int, end_line: int = None):
        self.name = name
        self.start_line = start_line
        self.end_line = end_line


class FileSummary:
    def __init__(self):
        self.classes = []
        self.methods = []

    def add_class(self, class_name: str, class_start_line: int, class_end_line: int = None):
        self.classes.append(SummaryPosition(class_name, class_start_line, class_end_line))

    def add_method(self, method_name: str, method_start_line: int, method_end_line: int = None):
        self.methods.append(SummaryPosition(method_name, method_start_line, method_end_line))


class CodeParser(ABC):
    @staticmethod
    def get_summary_from_position(
            summary_positions: List[SummaryPosition],
            start_line: int,
            end_line: int
    ) -> Tuple[List[SummaryPosition], List[SummaryPosition]]:

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
    def get_closest_method_class_in_snippet(
            file_summary: FileSummary,
            snippet_start_line: int,
            snippet_end_line: int
    ) -> str:
        closest_method_class_summary = ""

        last_class, current_class = CodeParser.get_summary_from_position(file_summary.classes, snippet_start_line,
                                                                         snippet_end_line)

        if last_class:
            closest_method_class_summary += f"  The last class defined before this snippet was called " \
                                            f"`{last_class[-1].name}` starting at line {last_class[-1].start_line} " \
                                            f"and ending at line {last_class[-1].end_line}."
        if len(current_class) == 1:
            closest_method_class_summary += f"  The class defined in this snippet is called `{current_class[0].name}`" \
                                            f"starting at line {current_class[0].start_line} and ending at line " \
                                            f"{current_class[0].end_line}."
        elif len(current_class) > 1:
            multi_class_summary = " and ".join(
                [f"`{c.name}` starting at line {c.start_line} and ending at line {c.end_line}" for c in current_class])
            closest_method_class_summary += f"  The classes defined in this snippet are {multi_class_summary}."

        last_method, current_method = CodeParser.get_summary_from_position(file_summary.methods, snippet_start_line,
                                                                           snippet_end_line)

        if last_method:
            closest_method_class_summary += f"  The last method starting before this snippet is called " \
                                            f"`{last_method[-1].name}` which starts on line " \
                                            f"{last_method[-1].start_line} and ends at line {last_method[-1].end_line}."
        if len(current_method) == 1:
            closest_method_class_summary += f"  The method defined in this snippet is called " \
                                            f"`{current_method[0].name}` starting at line " \
                                            f"{current_method[0].start_line} and ending at line " \
                                            f"{current_method[0].end_line}."
        elif len(current_method) > 1:
            multi_method_summary = " and ".join(
                [f"`{meth.name}` starting at line {meth.start_line} and ending at line {meth.end_line}" for meth in
                 current_method])
            closest_method_class_summary += f"  The methods defined in this snippet are {multi_method_summary}."

        return closest_method_class_summary

    @staticmethod
    @abstractmethod
    def get_file_summary(code: str, file_name: str) -> FileSummary:
        """Given a code string, parse and return important aspects of the code"""
