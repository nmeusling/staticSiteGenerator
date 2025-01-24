import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        html = HTMLNode()
        props = html.props_to_html()
        self.assertEqual(props, "")

    def test_props_to_html_one_prop(self):
        html = HTMLNode(props={"abc": "defg"})
        props = html.props_to_html()
        expected_props = 'abc="defg"'
        self.assertEqual(props, expected_props)

    def test_props_to_html_multiple_props(self):
        html = HTMLNode(props={"abc": "defg", "hij": "klmn"})
        props = html.props_to_html()
        expected_props = 'abc="defg" hij="klmn"'
        self.assertEqual(props, expected_props)