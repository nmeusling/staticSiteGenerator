import unittest

from markdown_tools.extract_blocks import markdown_to_blocks

class TestExtractBlocks(unittest.TestCase):
    def test_blocks_extracted(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        blocks = markdown_to_blocks(markdown)
        expected = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", 
        "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
        self.assertEqual(blocks, expected)

    def test_empty_block(self):
        markdown = ""
        blocks = markdown_to_blocks(markdown)
        expected = [""]
        self.assertEqual(blocks, expected)

    def test_blank_blocks_removed(self):
        markdown = "# This is a heading\n\n\n\n\nThis is a paragraph!\n\n\nOne last paragraph\n\n"
        blocks = markdown_to_blocks(markdown)
        expected = ["# This is a heading", "This is a paragraph!", "One last paragraph"]
        self.assertEqual(blocks, expected)

    def test_white_space_is_stripped(self):
        markdown = "    # This is a heading with leading and final whitespace    \n\n    Another paragraph.\n\nOne final paragraph    "
        blocks = markdown_to_blocks(markdown)
        expected = ["# This is a heading with leading and final whitespace", "Another paragraph.",  "One final paragraph"]
        self.assertEqual(blocks, expected)