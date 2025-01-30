import unittest

from nodes.textnode import TextNode, TextType, text_node_to_html_node
from nodes.leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq_no_url(self):
        node = TextNode("test one", TextType.CODE)
        node2 = TextNode("test one", TextType.CODE)
        self.assertEqual(node, node2)

    def test_eq(self):
        node = TextNode("test", TextType.IMAGE, "www.google.com")
        node2 = TextNode("test", TextType.IMAGE, "www.google.com")
        self.assertEqual(node, node2)
        
    def test_not_eq_url(self):
        node = TextNode("test one", TextType.ITALIC)
        node2 = TextNode("test one",TextType.ITALIC, "www.google.com" )
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("test", TextType.BOLD)
        node2 = TextNode("test", TextType.LINK)
        self.assertNotEqual(node, node2)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_invalid_text_type(self):
        text_node = TextNode("test", "invalid")
        with self.assertRaises(TypeError):
            text_node_to_html_node(text_node)

    def test_convert_bold(self):
        text_node = TextNode("test", TextType.BOLD)
        expected = LeafNode("b", "test")
        self.assertEqual(text_node_to_html_node(text_node), expected)

    def test_convert_image(self):
        text_node = TextNode("hello", TextType.IMAGE, url="www.test.com")
        expected = LeafNode("img", "", {"src": "www.test.com", "alt": "hello"})
        self.assertEqual(text_node_to_html_node(text_node), expected)
