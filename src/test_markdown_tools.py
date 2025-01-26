import unittest


from textnode import TextNode, TextType

from markdown_tools import split_nodes_delimiter, extract_markdown_images

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_node_split(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)

    def test_single_node_multiple_splits(self):
        node = TextNode("This is text with `two different` sections of `code blocks`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with ", TextType.NORMAL),
            TextNode("two different", TextType.CODE),
            TextNode(" sections of ", TextType.NORMAL),
            TextNode("code blocks", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_single_node_starting_with_delimitar(self):
        node = TextNode("**This is text that** starts with delimiter", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text that", TextType.BOLD),
            TextNode(" starts with delimiter", TextType.NORMAL)
        ]
        self.assertEqual(new_nodes, expected)

    def test_chaining_delimiters(self):
        node = TextNode("This *starts italic* and **then goes bold**", TextType.NORMAL)
        temp = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(temp, "*", TextType.ITALIC)
        expected = [
            TextNode("This ", TextType.NORMAL),
            TextNode("starts italic", TextType.ITALIC),
            TextNode(" and ", TextType.NORMAL),
            TextNode("then goes bold", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_nodes(self):
        nodes = [
            TextNode("This has no delimiters", TextType.NORMAL),
            TextNode("This is already bold", TextType.BOLD),
            TextNode("This should be split for *italic* into *several* nodes", TextType.NORMAL),
            TextNode("This also has a *single italic section* in it", TextType.NORMAL)
        ]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("This has no delimiters", TextType.NORMAL),
            TextNode("This is already bold", TextType.BOLD),
            TextNode("This should be split for ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" into ", TextType.NORMAL),
            TextNode("several", TextType.ITALIC),
            TextNode(" nodes", TextType.NORMAL),
            TextNode("This also has a ", TextType.NORMAL),
            TextNode("single italic section", TextType.ITALIC),
            TextNode(" in it", TextType.NORMAL)
        ]
        self.assertEqual(new_nodes, expected)

    def test_mismatched_delimiters(self):
        node = TextNode("This *starts italic and doesn't close", TextType.NORMAL)
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

    def test_text_type_normal(self):
        node = TextNode("This is already **bold** text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("This is already **bold** text", TextType.BOLD)]
        self.assertEqual(new_nodes, expected)

    def test_text_without_delimiter(self):
        node = TextNode("This has no delimiters", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("This has no delimiters", TextType.NORMAL)]
        self.assertEqual(new_nodes, expected)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "This is text with a ![alt text](www.source.url)"
        result = extract_markdown_images(text)
        expected = [("alt text", "www.source.url")]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text) 
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(result, expected)

    def test_no_images(self):
        text = "This is text with no images"
        result = extract_markdown_images(text) 
        expected = []
        self.assertEqual(result, expected)