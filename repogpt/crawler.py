import os
import fnmatch
from langchain.docstore.document import Document
from langchain.document_loaders import TextLoader
from langchain.text_splitter import Language
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from repogpt.parsers.pygments_parser import PygmentsParser
import logging

logger = logging.getLogger("repogpt_logger")

LANG_MAPPING = {
    '.py': Language.PYTHON,
    '.cpp': Language.CPP,
    '.cc': Language.CPP,
    '.cxx': Language.CPP,
    '.h': Language.CPP,
    '.hpp': Language.CPP,
    '.java': Language.JAVA,
    '.go': Language.GO,
    '.js': Language.JS,
    '.ts': Language.JS,
    '.php': Language.PHP,
    '.proto': Language.PROTO,
    '.rs': Language.RST,
    '.rb': Language.RUBY,
    '.scala': Language.SCALA,
    '.swift': Language.SWIFT,
    '.md': Language.MARKDOWN,
    '.tex': Language.LATEX,
    '.html': Language.HTML
}


def contains_hidden_dir(dir_path: str) -> bool:
    directories = dir_path.split('/')
    return any(fnmatch.fnmatch(directory, '.*') for directory in directories)


def process_file(file_contents: str, dir_path: str, file_name: str, extension: str, chunk_size: int = 3000,
                 chunk_overlap: int = 500) -> List[Document]:
    # get file summary for raw file
    summary = PygmentsParser.get_file_summary(file_contents, file_name)

    # if no summary was found by the parser, do not include it in the final chunk
    summary_str = ""
    if summary:
        summary_str = f"In this file there is a {', a '.join(summary)}."

    # split file contents based on file extension
    splitter = RecursiveCharacterTextSplitter.from_language(
        language=LANG_MAPPING[extension], chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True
    )
    split_docs = splitter.create_documents([file_contents])

    # add file path, starting line and summary to each chunk
    for doc in split_docs:
        starting_line = file_contents[:doc.metadata['start_index']].count('\n') + 1
        doc.page_content = f"The following code snippet is from a file at location \
{os.path.join(dir_path, file_name)} starting at line {starting_line}. {summary_str} " \
                           f"The code snippet starting at line {starting_line} is \n \
        ```\n{doc.page_content}\n```"

    return split_docs


def crawl(root_dir: str) -> List[Document]:
    docs = []
    for dir_path, dir_names, filenames in os.walk(root_dir):
        for file in filenames:
            _, extension = os.path.splitext(file)
            # only want to crawl accepted file types and files not in hidden directories
            if extension in LANG_MAPPING and not contains_hidden_dir(dir_path):
                try:
                    loader = TextLoader(os.path.join(dir_path, file), encoding='utf-8')
                    split_docs = process_file(loader.load(), dir_path, file, extension)
                    docs.extend(split_docs)
                except Exception as e:
                    logger.error(f"Error occurred while crawling repository. {e}")
    return docs
# from langchain.document_loaders import TextLoader
# import os
# from langchain.text_splitter import CharacterTextSplitter, PythonCodeTextSplitter
# import ast
# from langchain.embeddings import HuggingFaceEmbeddings
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#
# class Crawler:
#
#     def __init__(self, root_dir):
#         self.root_dir = root_dir
#         self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#
#
#     def _count_newlines(self, chunk:str, first_chunk_in_file:bool):
#         if not first_chunk_in_file:
#             return chunk.count('\n') +2
#         return chunk.count('\n') +1
#
#     def ord(self,n):
#         return str(n) + ("th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))
#
#     def _format_page_content(self, page_content:str, source:str, chunk_num:int, class_method_names:str):
#         new_page_content = f"The following is a code snippet from the file {source} with structure {class_method_names}.\n```\n{page_content}\n```"
#         return new_page_content
#
#     def get_class_and_method_names(self, filename:str):
#         with open(filename, 'r') as file:
#             content = file.read()
#         class_methods = {'<module>': []}  # for methods not part of classes
#
#         tree = ast.parse(content)
#
#         current_class = None
#
#         for node in ast.walk(tree):
#             if isinstance(node, ast.ClassDef):
#                 current_class = node.name
#                 class_methods[current_class] = []
#             elif isinstance(node, ast.FunctionDef):
#                 if current_class:
#                     class_methods[current_class].append(node.name)
#                 else:
#                     class_methods['<module>'].append(node.name)
#
#         output_string=""
#         for class_name, methods in class_methods.items():
#             output_string += f"Class: {class_name}\n"
#             for method_name in methods:
#                 output_string += f" - Method: {method_name}\n"
#             output_string += "\n"
#         print(output_string)
#         return output_string
#
#
#
#     def crawl(self):
#         docs = []
#         for dirpath, dirnames, filenames in os.walk(self.root_dir):
#             for file in filenames:
#                 if file.endswith('.py') and '/.venv/' not in dirpath:
#                     try:
#                         loader = TextLoader(os.path.join(dirpath, file), encoding='utf-8')
#                         #print(loader.load_and_split())
#                         docs.extend(loader.load_and_split())
#                     except Exception as e:
#                         pass
#         print(f'{len(docs)}')
#
#         text_splitter = PythonCodeTextSplitter(chunk_size=3000, chunk_overlap=500, add_start_index=True)
#         texts = text_splitter.split_documents(docs)
#
#         source = ""
#         chunk_num = 0
#
#         for text in texts:
#             if text.metadata['source']!= source:
#                 source = text.metadata['source']
#                 chunk_num = 0
#                 print(f"-------------------- new file: {text.metadata['source']} ---------------------------------")
#                 class_method_names = self.get_class_and_method_names(text.metadata['source'])
#
#             chunk_num+=1
#             text.metadata['chunk_num']=chunk_num
#             text.page_content = self._format_page_content(text.page_content, text.metadata['source'], text.metadata['chunk_num'], class_method_names)
#
#             print(text)
#
#
#         print(f"{len(texts)}")
#
#         #from langchain.embeddings.openai import OpenAIEmbeddings
#
#         #embeddings = OpenAIEmbeddings()
#
#         from langchain.embeddings import SentenceTransformerEmbeddings
#         embeddings = SentenceTransformerEmbeddings()
#
#         from langchain.vectorstores import DeepLake
#         # from embedding_tests import SentenceTransformEmbeddingsFixed
#         #
#         # embeddings = SentenceTransformEmbeddingsFixed()
#         db = DeepLake.from_documents(texts, embeddings, dataset_path="../vs/pandas10/")
#
#
#
# c = Crawler('../../pandas')
# c.crawl()
