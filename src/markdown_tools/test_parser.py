import unittest


from nodes.textnode import TextNode, TextType
from nodes.parentnode import ParentNode

from markdown_tools.parser import text_to_textnodes, markdown_to_html_node, get_heading_level_tag


class TestTextToTextNodes(unittest.TestCase):
    def test_one_of_each_type(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

class TestGetHeadingLevel(unittest.TestCase):
    def test_level_one(self):
        text = "# Heading 1"
        self.assertEqual(get_heading_level_tag(text), "h1")

    def test_level_six(self):
        text = "###### Heading 6"
        self.assertEqual(get_heading_level_tag(text), "h6")


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_only_paragraphs(self):
        text = "This is **markdown** with some *inline*\n\nIt also has several simple paragraph **blocks**"
        expected = ParentNode("div", [
            ParentNode("p", [
                TextNode("This is ", TextType.NORMAL),
                TextNode("markdown", TextType.BOLD),
                TextNode(" with some ", TextType.NORMAL),
                TextNode("inline", TextType.ITALIC)
            ]), 
            ParentNode("p", [
                TextNode("It also has several simple paragraph ", TextType.NORMAL),
                TextNode("blocks", TextType.BOLD)
            ])
        ])
        result = markdown_to_html_node(text)
        self.assertEqual(result, expected)

    def test_one_paragraph_all_inline_types(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = ParentNode("div", [
            ParentNode("p", [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ])
        ])
        result = markdown_to_html_node(text)
        self.assertEqual(result, expected)

    def test_various_heading_level_blocks(self):
        text = "# Heading 1\n\n## Heading 2\n\n###### Heading 6"
        expected = ParentNode("div", [
            ParentNode("h1", [
                TextNode("Heading 1", TextType.NORMAL)
            ]),
            ParentNode("h2", [
                TextNode("Heading 2", TextType.NORMAL)
            ]),
            ParentNode("h6", [
                TextNode("Heading 6", TextType.NORMAL)
            ])
        ])
        result = markdown_to_html_node(text)
        print(result)
        self.assertEqual(result, expected)

    def test_code_block(self):
        text = """```
        def function(parameter):
            do_something();
        ```"""
        