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