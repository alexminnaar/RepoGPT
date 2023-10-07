from repogpt.parsers.treesitter import TreeSitterParser, FileSummary, SummaryPosition
from tree_sitter import Language, Parser


class JavaTreeSitterParser(TreeSitterParser):
    @staticmethod
    def get_file_summary(code: str, file_name: str) -> FileSummary:

        if not TreeSitterParser.loaded:
            TreeSitterParser.initialize_treesitter()

        file_summary = FileSummary()
        parser = Parser()
        parser.set_language(TreeSitterParser.languages['java'])
        tree = parser.parse(bytes(code, "utf-8"))

        def traverse(node, current_line):
            if node.type == 'constructor_declaration':
                for child in node.children:
                    if child.type == 'identifier':
                        function_name = code[child.start_byte: child.end_byte]
                        file_summary.methods.append(
                            SummaryPosition(function_name, node.start_point[0], node.end_point[0]))

            if node.type == 'method_declaration':
                for child in node.children:
                    if child.type == 'identifier':
                        function_name = code[child.start_byte: child.end_byte]
                        file_summary.methods.append(
                            SummaryPosition(function_name, node.start_point[0], node.end_point[0]))

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
