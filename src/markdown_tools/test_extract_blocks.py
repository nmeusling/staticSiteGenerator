import unittest

from markdown_tools.extract_blocks import markdown_to_blocks, block_to_block_type, BlockTypes

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
        expected = []
        self.assertEqual(blocks, expected)

    def test_blank_blocks_removed(self):
        markdown = "# This is a heading\n\n\n\n\nThis is a paragraph!\n\n\nOne last paragraph\n\n\n\nAnd one more\n\n\n"
        blocks = markdown_to_blocks(markdown)
        expected = ["# This is a heading", "This is a paragraph!", "One last paragraph", "And one more"]
        self.assertEqual(blocks, expected)

    def test_white_space_is_stripped(self):
        markdown = "    # This is a heading with leading and final whitespace    \n\n    Another paragraph.\n\nOne final paragraph    "
        blocks = markdown_to_blocks(markdown)
        expected = ["# This is a heading with leading and final whitespace", "Another paragraph.",  "One final paragraph"]
        self.assertEqual(blocks, expected)

class TestBlockToHeader(unittest.TestCase):
    def test_top_level_header(self):
        block = "# header"
        expected_block_type = BlockTypes.HEADING
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected_block_type)

    def test_mid_level_header(self):
        block = "### header"
        expected_block_type = BlockTypes.HEADING
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected_block_type)

    def test_header_no_space(self):
        block = "#header"
        expected_block_type = BlockTypes.PARAGRAPH
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected_block_type)

    def test_too_many_levels_header(self):
        block = "####### header"
        expected_block_type = BlockTypes.PARAGRAPH
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected_block_type)

class TestBlockToCode(unittest.TestCase):
    def test_start_and_end_code(self):
        block = r"```test code; \n more lines;\n one more```"
        expected_block_type = BlockTypes.CODE
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected_block_type)

    def test_start_code(self):
        block = r"``` test code"
        expected_block_type = BlockTypes.PARAGRAPH
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected_block_type)
    
    def test_end_code(self):
        block = r"header```"
        expected_block_type = BlockTypes.PARAGRAPH
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected_block_type)
    
    def test_ticks_not_first_characters(self):
        block = r"t```test code; \n more lines;\n one more```"
        expected_block_type = BlockTypes.PARAGRAPH
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected_block_type)