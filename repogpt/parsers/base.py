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
    @abstractmethod
    def get_summary_from_position(summary_positions: List[SummaryPosition], start_line: int,
                                  end_line: int) -> Tuple[List[SummaryPosition], List[SummaryPosition]]:
        """Helper function to get object positions within snippet"""

    @staticmethod
    @abstractmethod
    def get_closest_method_class_in_snippet(file_summary: FileSummary, snippet_start_line: int,
                                            snippet_end_line: int) -> str:
        """Get the relevent methods and classes in a snippet and convert to prompt"""

    @staticmethod
    @abstractmethod
    def get_file_summary(code: str, file_name: str) -> FileSummary:
        """Given a code string, parse and return important aspects of the code"""
