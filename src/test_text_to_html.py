import unittest

from text_to_html import text_node_to_html_node
from textnode import TextNode, TextType
from leafnode import LeafNode

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
