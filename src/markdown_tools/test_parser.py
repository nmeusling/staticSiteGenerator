import unittest


from nodes.textnode import TextNode, TextType
from nodes.parentnode import ParentNode

from markdown_tools.parser import text_to_textnodes, markdown_to_html_node, get_heading_level_tag, remove_formatting
from markdown_tools.extract_blocks import BlockTypes

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


class TestRemoveFormatting(unittest.TestCase):
    def test_heading(self):
        text = "### Heading"
        expected = "Heading"
        result = remove_formatting(text, BlockTypes.HEADING)
        self.assertEqual(result, expected)

    def test_code(self):
        text = """```
def test():
    do_something()
```"""
        expected = """
def test():
    do_something()
"""
        result = remove_formatting(text, BlockTypes.CODE)
        self.assertEqual(result, expected)

    def test_quote(self):
        text = """>first line of quote
>second line of quote"""
        expected = "first line of quote\nsecond line of quote"
        result = remove_formatting(text, BlockTypes.QUOTE)
        self.assertEqual(result, expected)

    def test_ordered_list(self):
        text = """1. test
2. test
12. test"""
        expected = "test\ntest\ntest"
        result = remove_formatting(text, BlockTypes.ORDERED_LIST)
        self.assertEqual(result, expected)

    def test_ordered_list(self):
        text = """- test
* test
- test"""
        expected = "test\ntest\ntest"
        result = remove_formatting(text, BlockTypes.UNORDERED_LIST)
        self.assertEqual(result, expected)

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
        self.assertEqual(result, expected)

    def test_code_block(self):
        text = """```
def function():
    do_something();
```"""
        expected = ParentNode("div", [
            ParentNode("pre", [
                ParentNode("code", [
                    TextNode("""
def function():
    do_something();
""", TextType.NORMAL)
                ])
            ])
        ])
        result = markdown_to_html_node(text)
        self.assertEqual(result, expected)
        
    def test_quote_block(self):
        text = ">This is one quote line\n>This is another quote line\n>And a third quote line><"
        expected = ParentNode("div", [
            ParentNode("blockquote", [
                TextNode("This is one quote line\nThis is another quote line\nAnd a third quote line><", TextType.NORMAL)
            ])
        ])
        result = markdown_to_html_node(text)
        self.assertEqual(result, expected)

    def test_unordered_list_block(self):
        text = """- first item
* second item
- third item
* fourth item
"""
        expected = ParentNode("div", [
            ParentNode("ul", [
                ParentNode("li", [
                    TextNode("first item", TextType.NORMAL)
                ]),
                ParentNode("li", [
                    TextNode("second item", TextType.NORMAL)
                ]),
                ParentNode("li", [
                    TextNode("third item", TextType.NORMAL)
                ]),
                ParentNode("li", [
                    TextNode("fourth item", TextType.NORMAL)
                ]),
            ])
        ])
        result = markdown_to_html_node(text)
        self.assertEqual(result, expected)

    def test_ordered_list_block(self):
        text = """2. first item
2. second item
2. third item
2. fourth item
"""
        expected = ParentNode("div", [
            ParentNode("ol", [
                ParentNode("li", [
                    TextNode("first item", TextType.NORMAL)
                ]),
                ParentNode("li", [
                    TextNode("second item", TextType.NORMAL)
                ]),
                ParentNode("li", [
                    TextNode("third item", TextType.NORMAL)
                ]),
                ParentNode("li", [
                    TextNode("fourth item", TextType.NORMAL)
                ]),
            ])
        ])
        result = markdown_to_html_node(text)
        self.assertEqual(result, expected)

    def test_large_markdown_with_all_block_types_including_inline(self):
        text = """
        # Heading with *italic*

        ### Lower Heading
        
        This is a simple paragraph that has **bold** and *italic*.

        This is another paragraph that has [link](www.test.com) and ![image](www.source.com). Very cool!

        >This is a quote box. 
        >Another line of the quote.

        ### Code Example

        ```
        def do_something():
            print("Hello World")
        ```



        - list item one with **bold**
        * list item two with *italic*
        - list item with `code`

        This is another paragraph that has small `code section in it`

        1. Ordered list with **bold** is very cool
        2. Ordered list with nothing special
        """
        expected = ParentNode("div", [
            ParentNode("h1", [
                TextNode("Heading with ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC)
            ]),
            ParentNode("h3", [
                TextNode("Lower Heading", TextType.NORMAL)
            ]),
            ParentNode("p", [
                TextNode("This is a simple paragraph that has ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(".", TextType.NORMAL)
            ]),
            ParentNode("p", [
                TextNode("This is another paragraph that has ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "www.test.com"),
                TextNode(" and ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "www.source.com"),
                TextNode(". Very cool!", TextType.NORMAL)
            ]),
            ParentNode("blockquote", [
                TextNode("This is a quote box. Another line of the quote.", TextType.NORMAL)
            ]),
            ParentNode("h3", [
                TextNode("Code Example", TextType.NORMAL)
            ]),
            ParentNode("pre", [
                ParentNode("code", [
                    TextNode("""def do_something():
    print("Hello World")""", TextType.NORMAL)])
            ]),
            ParentNode("ul", [
                ParentNode("li", [
                    TextNode("list item one with ", TextType.NORMAL),
                    TextNode("bold", TextType.BOLD)
                ]),
                ParentNode("li", [
                    TextNode("list item two with ", TextType.NORMAL),
                    TextNode("italic", TextType.ITALIC)
                ]),
                ParentNode("li", [
                    TextNode("list item two with ", TextType.NORMAL),
                    TextNode("code", TextType.CODE)
                ])
        
            ]),
            ParentNode("p", [
                TextNode("This is another paragraph that has small ", TextType.NORMAL),
                TextNode("code section in it", TextType.CODE)
            ]),
            ParentNode("ol", [
                ParentNode("li", [
                    TextNode("Ordered list with ", TextType.NORMAL),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" is very cool", TextType.NORMAL)
                ]),
                ParentNode("li", [
                    TextNode("Ordered list with nothing special", TextType.NORMAL),
                ])
            ])
        ])    