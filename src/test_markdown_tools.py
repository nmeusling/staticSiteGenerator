import unittest


from textnode import TextNode, TextType

from markdown_tools import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link

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
    
    def test_link_not_extracted_as_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) [other](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_text_that_starts_with_image(self):
        text = "![alt text](www.source.url)"
        expected = [("alt text", "www.source.url")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "This is text with a [link text](www.source.url)"
        result = extract_markdown_links(text)
        expected = [("link text", "www.source.url")]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        text = "This is text with a [two links](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_links(text) 
        expected = [("two links", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(result, expected)

    def test_no_links(self):
        text = "This is text with no links"
        result = extract_markdown_links(text) 
        expected = []
        self.assertEqual(result, expected)
    
    def test_image_not_extracted_as_link(self):
        text = "This is text with a [rick roll](www.test.com) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) [other](www.other.com)"
        expected = [("rick roll", "www.test.com"), ("other", "www.other.com")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_text_that_starts_with_link(self):
        text = "[link text](www.test.com)"
        expected = [("link text", "www.test.com")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

class TestSplitNodesLink(unittest.TestCase):
    def test_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_links_start_middle_end(self):
        node = TextNode(
            "[This](www.link.com) is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This", TextType.LINK, "www.link.com"),
            TextNode(" is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_single_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) only",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" only", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_single_link_at_end(self):

        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_single_link_at_start(self):
        node = TextNode(
            "[Starting link](https://www.boot.dev) with text",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Starting link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" with text", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_single_link_only(self):
        node = TextNode(
            "[Starting link](https://www.boot.dev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Starting link", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertEqual(new_nodes, expected)