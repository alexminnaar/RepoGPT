import unittest
from repogpt.crawler import process_file, contains_hidden_dir
from langchain.docstore.document import Document


class CrawlerTestCase(unittest.TestCase):

    def test_process_file(self):
        PYTHON_CODE = """
def hello_world():
    print("Hello, World!")

# Call the function
hello_world()
        """

        docs = process_file([Document(page_content=PYTHON_CODE)], "/my/file/path/", "hello.py",
                            ".py", 100, 0)

        expected_docs = [Document(page_content='The following code snippet is from a file at location '
                                               '/my/file/path/hello.py starting at line 2 and ending at line 6.   '
                                               'The method defined in this snippet is called `hello_world` starting at '
                                               'line 2 and ending at line 3. The code snippet starting at line 2 and '
                                               'ending at line 6 is \n ```\ndef hello_world():\n    '
                                               'print("Hello, World!")\n\n# Call the function\nhello_world()\n``` ',
                                  metadata={'start_index': 1, 'starting_line': 2, 'ending_line': 6}),]
        assert expected_docs == docs

    def test_contains_hidden_dir_is_hidden(self):
        test_contains = contains_hidden_dir("/my/test/.hidden/dir")
        assert test_contains

    def test_contains_hidden_dir_not_hidden(self):
        test_contains = contains_hidden_dir("/my/test/dir")
        assert not test_contains
