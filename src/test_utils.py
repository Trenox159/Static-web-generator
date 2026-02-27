import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from utils import split_nodes_delimiter

class TestUtils(unittest.TestCase):
    def test_code_text(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(str(new_nodes), '[TextNode(This is text with a , TextType.TEXT, None), TextNode(code block, TextType.CODE_TEXT, None), TextNode( word, TextType.TEXT, None)]')

    def test_italic(self):
        node = TextNode("This is text with a _code block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.CODE_TEXT)
        self.assertEqual(str(new_nodes), '[TextNode(This is text with a , TextType.TEXT, None), TextNode(code block, TextType.ITALIC, None), TextNode( word, TextType.TEXT, None)]')

    def test_bold(self):
        node = TextNode("This is text with a *code block* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.CODE_TEXT)
        self.assertEqual(str(new_nodes), '[TextNode(This is text with a , TextType.TEXT, None), TextNode(code block, TextType.BOLD, None), TextNode( word, TextType.TEXT, None)]')

if __name__ == "__main__":
    unittest.main()
