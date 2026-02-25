import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_print(self):
        node = HTMLNode('p', 'test file', [], {'test': "asdasd"})
        self.assertEqual(node.__repr__(), 'HTMLNode(p, test file, [], {\'test\': \'asdasd\'})')

    def test_props(self):
        node = HTMLNode('p', 'test file', [], {'test': "asdasd", 'test2' : "aaa"})
        props = node.props_to_html()
        self.assertEqual(props, ' test="asdasd" test2="aaa"')

    def test_props2(self):
        node = HTMLNode('p', 'test file', [])
        props = node.props_to_html()
        self.assertEqual(props, '')


class TestLeafNode(unittest.TestCase):
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()
