import unittest
from repogpt.parsers.treesitter_parser import TreeSitterParser
from repogpt.parsers.base import SummaryPosition


class TreeSitterParserTest(unittest.TestCase):

    def test_treesitter_parser_cpp(self):
        cpp_code = '''
        #include <iostream>
        using namespace std;

        class MyClass {
        public:
            void greet() {
                cout << "Hello!" << endl;
            }
        };
        '''

        tsp = TreeSitterParser()
        fs = tsp.get_file_summary(cpp_code, "test.cpp")

        expected_methods = [SummaryPosition("greet()", 6, 8)]
        expected_classes = [SummaryPosition("MyClass", 4, 9)]

        assert expected_methods[0].name == fs.methods[0].name \
               and expected_methods[0].start_line == fs.methods[0].start_line \
               and expected_methods[0].end_line == fs.methods[0].end_line \
               and expected_classes[0].name == fs.classes[0].name \
               and expected_classes[0].start_line == fs.classes[0].start_line \
               and expected_classes[0].end_line == fs.classes[0].end_line

    def test_treesitter_parser_java(self):
        java_code = """
public class IntegerSequenceTest {
    @Test
    public void testRangeMultipleIterations() {
        // Check that we can iterate several times using the same instance.
        final int start = 1;
        final int max = 7;
        final int step = 2;

        final List<Integer> seq = new ArrayList<>();
        final IntegerSequence.Range r = IntegerSequence.range(start, max, step);

        final int numTimes = 3;
        for (int n = 0; n < numTimes; n++) {
            seq.clear();
            for (Integer i : r) {
                seq.add(i);
            }
            Assert.assertEquals(4, seq.size());
            Assert.assertEquals(seq.size(), r.size());
        }
    }
        """

        tsp = TreeSitterParser()
        fs = tsp.get_file_summary(java_code, "test.java")

        expected_methods = [SummaryPosition("testRangeMultipleIterations", 2, 21)]

        assert expected_methods[0].name == fs.methods[0].name \
               and expected_methods[0].start_line == fs.methods[0].start_line \
               and expected_methods[0].end_line == fs.methods[0].end_line
