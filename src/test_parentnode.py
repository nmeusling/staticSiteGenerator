import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_no_tag(self):
        node = ParentNode(None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_no_children(self):
        node = ParentNode("a", None)
        self.assertRaises(ValueError, node.to_html)

    def test_no_children_empty_list(self):
        node = ParentNode("a", [])
        self.assertRaises(ValueError, node.to_html)

    def test_one_child(self):
        parent = ParentNode("p", [LeafNode("b", "Bold text")])
        expected = '<p><b>Bold text</b></p>'
        self.assertEqual(parent.to_html(), expected)

    def test_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected ="<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_multiple_layers(self):
        grandparent = ParentNode("p", 
            [
                ParentNode("p", 
                [
                    LeafNode(None, "123"), 
                    LeafNode("p", "456"), 
                    LeafNode("a", "123", {"href": "abc"})
                ],
                {"zyx": "wuv"}), 
                ParentNode("h4", 
                [
                    LeafNode(None, "Test text"), 
                    LeafNode("h5", "Header", {"value": "test"})
                ])
            ], 
            {"mno": "pqr"})
        expected = '<p mno="pqr"><p zyx="wuv">123<p>456</p><a href="abc">123</a></p><h4>Test text<h5 value="test">Header</h5></h4></p>'
        self.assertEqual(grandparent.to_html(), expected)

    def test_parent_node_with_one_prop(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ],
            {"value": "123"}
        )
        expected ='<p value="123"><b>Bold text</b>Normal text</p>'
        self.assertEqual(node.to_html(), expected)

    def test_parent_node_with_two_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ],
            {"value": "123", "href": "456"}
        )
        expected ='<p value="123" href="456"><b>Bold text</b>Normal text</p>'
        self.assertEqual(node.to_html(), expected)