import unittest

from nodes.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_no_value(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_no_tags(self):
        node = LeafNode(None, "test")
        expected = "test"
        self.assertEqual(node.to_html(), expected)

    def test_one_prop(self):
        node = LeafNode("a", "click me", {"href": "www.google.com"})
        expected = '<a href="www.google.com">click me</a>'
        self.assertEqual(node.to_html(), expected)

    def test_no_props(self):
        node = LeafNode("p", "test")
        expected = '<p>test</p>'
        self.assertEqual(node.to_html(), expected)
    
    def test_two_props(self):
        node = LeafNode("a", "click me", {"href": "www.google.com", "ab": "def"})
        expected = '<a href="www.google.com" ab="def">click me</a>'
        self.assertEqual(node.to_html(), expected)
    