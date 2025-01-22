import unittest

from textnode import TextNode, TextType


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
    