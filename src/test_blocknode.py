import unittest

from blocknode import block_to_block_type, BlockType
from utils import markdown_to_blocks


class TestBlockNode(unittest.TestCase):

    def test_headings(self):
        result = block_to_block_type('## This is **bolded** paragraph')
        result2 = block_to_block_type('####### This is **bolded** paragraph')
        self.assertEqual(result, BlockType.HEADING)
        self.assertEqual(result2, BlockType.PARAGRAPH)

    def test_code_blocks(self):
        result = block_to_block_type('```\nthis is python code\n```')
        result2 = block_to_block_type('``\nthis is python code\n``')
        self.assertEqual(result, BlockType.CODE)
        self.assertEqual(result2, BlockType.PARAGRAPH)

    def test_quote_block(self):
        result = block_to_block_type('> "I am in fact a Hobbit in all but size."\n>\n> -- J.R.R. Tolkien')
        result2 = block_to_block_type('>asdasdasdasdasdasdad\n>asdasdasdasd\nasdasd')
        self.assertEqual(result, BlockType.QUOTE)
        self.assertEqual(result2, BlockType.PARAGRAPH)

    def test_unordered_list(self):
        result = block_to_block_type('- asdasdasd\n- asdasddd\n- asdasd')
        result2 = block_to_block_type('- asdasdasd\n- asdasddd\n-asdasd')
        self.assertEqual(result, BlockType.UNORD_LIST)
        self.assertEqual(result2, BlockType.PARAGRAPH)

    def test_ordered_list(self):
        result = block_to_block_type('1. asdasdasd\n2. asdasddd\n3. asdasd')
        result2 = block_to_block_type('1. asdasdasd\n5. asdasddd\n4. asdasd')
        self.assertEqual(result, BlockType.ORD_LIST)
        self.assertEqual(result2, BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
