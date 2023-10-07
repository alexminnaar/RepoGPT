from repogpt.parsers.treesitter import TreeSitterParser, FileSummary, SummaryPosition
import ast


class PythonParser(TreeSitterParser):

    @staticmethod
    def get_file_summary(code: str, file_name:str) -> FileSummary:
        """Get the classes and methods in python code."""
        parsed_tree = ast.parse(code)
        file_summary = FileSummary()

        # Traverse the AST to find function and class definitions
        for node in ast.walk(parsed_tree):
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                function_start_line = node.lineno
                function_end_line = node.end_lineno
                file_summary.methods.append(
                    SummaryPosition(function_name, function_start_line, function_end_line))

            elif isinstance(node, ast.ClassDef):
                class_name = node.name
                class_start_line = node.lineno
                class_end_line = node.end_lineno
                file_summary.classes.append(
                    SummaryPosition(class_name, class_start_line, class_end_line))

        # methods and classes are not in order so sort
        file_summary.methods = sorted(file_summary.methods, key=lambda x: x.start_line)
        file_summary.classes = sorted(file_summary.classes, key=lambda x: x.start_line)

        return file_summary
