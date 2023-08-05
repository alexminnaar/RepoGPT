from repogpt.parsers.base import CodeParser, FileSummary, SummaryPosition
import subprocess
from tree_sitter import Language, Parser
import os


class TreeSitterParser(CodeParser):
    languages = {}
    loaded = False

    @staticmethod
    def initialize_treesitter():
        # download tree-sitter shared objects according to
        # https://github.com/sweepai/sweep/blob/b267b613d4c706eaf959fe6789f11e9a856521d1/sweepai/utils/utils.py#L169
        LANGUAGE_NAMES = ["python", "java", "cpp", "go", "rust", "ruby", "php"]
        for language in LANGUAGE_NAMES:
            subprocess.run(
                f"git clone https://github.com/tree-sitter/tree-sitter-{language} cache/tree-sitter-{language}",
                shell=True)
        for language in LANGUAGE_NAMES:
            Language.build_library(f'cache/build/{language}.so', [f"cache/tree-sitter-{language}"])
            subprocess.run(f"cp cache/build/{language}.so /tmp/{language}.so", shell=True)
        TreeSitterParser.languages = {language: Language(f"/tmp/{language}.so", language) for language in
                                      LANGUAGE_NAMES}
        subprocess.run(f"git clone https://github.com/tree-sitter/tree-sitter-c-sharp cache/tree-sitter-c-sharp",
                       shell=True)
        Language.build_library(f'cache/build/c-sharp.so', [f"cache/tree-sitter-c-sharp"])
        subprocess.run(f"cp cache/build/c-sharp.so /tmp/c-sharp.so", shell=True)
        TreeSitterParser.languages["c-sharp"] = Language("/tmp/c-sharp.so", "c_sharp")

        subprocess.run(f"git clone https://github.com/tree-sitter/tree-sitter-typescript cache/tree-sitter-typescript",
                       shell=True)
        Language.build_library(f'cache/build/typescript.so', [f"cache/tree-sitter-typescript/tsx"])
        subprocess.run(f"cp cache/build/typescript.so /tmp/typescript.so", shell=True)
        TreeSitterParser.languages["tsx"] = Language("/tmp/typescript.so", "tsx")
        TreeSitterParser.loaded = True

    @staticmethod
    def get_file_summary(code: str, file_name: str) -> FileSummary:

        # download and build treesitter shared objects if not already done.
        if not TreeSitterParser.loaded:
            TreeSitterParser.initialize_treesitter()

        extension_to_language = {
            ".py": "python",
            ".rs": "rust",
            ".go": "go",
            ".java": "java",
            ".cpp": "cpp",
            ".cc": "cpp",
            ".cxx": "cpp",
            ".c": "cpp",
            ".h": "cpp",
            ".hpp": "cpp",
            ".rb": "ruby",
            ".php": "php",
            ".js": "tsx",
            ".jsx": "tsx",
            ".ts": "tsx",
            ".tsx": "tsx",
            ".mjs": "tsx",
            ".cs": "c-sharp",

        }

        file_summary = FileSummary()
        _, extension = os.path.splitext(file_name)

        if extension in extension_to_language:
            language = TreeSitterParser.languages[extension_to_language[extension]]
            parser = Parser()
            parser.set_language(language)
            tree = parser.parse(bytes(code, "utf-8"))

            def traverse(node, current_line):

                if node.type == 'function_definition':
                    function_name_node = node.children[1]
                    function_name = code[function_name_node.start_byte: function_name_node.end_byte]
                    file_summary.methods.append(SummaryPosition(function_name, node.start_point[0], node.end_point[0]))

                if node.type == 'function_declaration':
                    for child in node.children:
                        if child.type == 'identifier':
                            function_name = code[child.start_byte: child.end_byte]
                            file_summary.methods.append(
                                SummaryPosition(function_name, node.start_point[0], node.end_point[0]))

                if node.type == 'constructor_declaration':
                    function_name_node = node.children[1]
                    function_name = code[function_name_node.start_byte: function_name_node.end_byte]
                    file_summary.methods.append(SummaryPosition(function_name, node.start_point[0], node.end_point[0]))

                if node.type == 'method_declaration':
                    for child in node.children:
                        if child.type == 'identifier':
                            function_name = code[child.start_byte: child.end_byte]
                            file_summary.methods.append(
                                SummaryPosition(function_name, node.start_point[0], node.end_point[0]))

                if node.type == 'class_specifier':
                    class_name_node = node.children[1]
                    class_name = code[class_name_node.start_byte: class_name_node.end_byte]
                    file_summary.classes.append(SummaryPosition(class_name, node.start_point[0], node.end_point[0]))

                if node.type == 'class_declaration':
                    for child in node.children:
                        if child.type == 'identifier':
                            class_name = code[child.start_byte: child.end_byte]
                            file_summary.classes.append(
                                SummaryPosition(class_name, node.start_point[0], node.end_point[0]))

                for child in node.children:
                    traverse(child, current_line)

            root_node = tree.root_node

            traverse(root_node, 0)

            # methods and classes are not in order so sort
            file_summary.methods = sorted(file_summary.methods, key=lambda x: x.start_line)
            file_summary.classes = sorted(file_summary.classes, key=lambda x: x.start_line)

        return file_summary
