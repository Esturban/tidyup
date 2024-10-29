import unittest
from unittest.mock import patch
from tidyup.utils import parse_arguments

class TestParseArguments(unittest.TestCase):

    @patch('sys.argv', ['tidyup', '-e', '/path/to/dir'])
    def test_parse_arguments_extension(self):
        args = parse_arguments()
        self.assertTrue(args.e)
        self.assertFalse(args.d)
        self.assertFalse(args.rearrange)
        self.assertEqual(args.directory, '/path/to/dir')
        self.assertEqual(args.depth, 2)

    @patch('sys.argv', ['tidyup', '-d', '/path/to/dir'])
    def test_parse_arguments_date(self):
        args = parse_arguments()
        self.assertFalse(args.e)
        self.assertTrue(args.d)
        self.assertFalse(args.rearrange)
        self.assertEqual(args.directory, '/path/to/dir')
        self.assertEqual(args.depth, 2)

    @patch('sys.argv', ['tidyup', '-ed', '/path/to/dir'])
    def test_parse_arguments_extension_date(self):
        args = parse_arguments()
        self.assertTrue(args.e)
        self.assertTrue(args.d)
        self.assertFalse(args.rearrange)
        self.assertEqual(args.directory, '/path/to/dir')
        self.assertEqual(args.depth, 2)

    @patch('sys.argv', ['tidyup', '-de', '/path/to/dir'])
    def test_parse_arguments_date_extension(self):
        args = parse_arguments()
        self.assertTrue(args.e)
        self.assertTrue(args.d)
        self.assertFalse(args.rearrange)
        self.assertEqual(args.directory, '/path/to/dir')
        self.assertEqual(args.depth, 2)

    @patch('sys.argv', ['tidyup', '-r', '-d', '-L', '3', '/path/to/dir'])
    def test_parse_arguments_rearrange_date_depth(self):
        args = parse_arguments()
        self.assertFalse(args.e)
        self.assertTrue(args.d)
        self.assertTrue(args.rearrange)
        self.assertEqual(args.directory, '/path/to/dir')
        self.assertEqual(args.depth, 3)

    @patch('sys.argv', ['tidyup', '-r', '-e', '-L', '4', '/path/to/dir'])
    def test_parse_arguments_rearrange_extension_depth(self):
        args = parse_arguments()
        self.assertTrue(args.e)
        self.assertFalse(args.d)
        self.assertTrue(args.rearrange)
        self.assertEqual(args.directory, '/path/to/dir')
        self.assertEqual(args.depth, 4)

    @patch('sys.argv', ['tidyup', '-r', '-ed', '-L', '5', '/path/to/dir'])
    def test_parse_arguments_rearrange_extension_date_depth(self):
        args = parse_arguments()
        self.assertTrue(args.e)
        self.assertTrue(args.d)
        self.assertTrue(args.rearrange)
        self.assertEqual(args.directory, '/path/to/dir')
        self.assertEqual(args.depth, 5)

    @patch('sys.argv', ['tidyup', '-r', '-de', '-L', '6', '/path/to/dir'])
    def test_parse_arguments_rearrange_date_extension_depth(self):
        args = parse_arguments()
        self.assertTrue(args.e)
        self.assertTrue(args.d)
        self.assertTrue(args.rearrange)
        self.assertEqual(args.directory, '/path/to/dir')
        self.assertEqual(args.depth, 6)
        
if __name__ == '__main__':
    unittest.main()