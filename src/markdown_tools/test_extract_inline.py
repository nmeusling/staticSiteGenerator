import unittest

from markdown_tools.extract_inline import extract_markdown_images, extract_markdown_links


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
