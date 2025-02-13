from enum import Enum
import re

class BlockTypes(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    blocks = [block for block in blocks if block]
    return blocks

def block_to_block_type(block):
    type_to_pattern = {
        BlockTypes.HEADING: "^[#]{1,6} ",
        BlockTypes.QUOTE: "^>",
        BlockTypes.UNORDERED_LIST: "^[-*] ",
        BlockTypes.ORDERED_LIST: "^\d. "
    }

    if re.search(type_to_pattern[BlockTypes.HEADING], block):
        return BlockTypes.HEADING
    if block[0:3] == "```" and block[-3:] == "```":
        return BlockTypes.CODE
    
    if lines_start_with_pattern(block, type_to_pattern[BlockTypes.QUOTE]):
        return BlockTypes.QUOTE
    if lines_start_with_pattern(block, type_to_pattern[BlockTypes.UNORDERED_LIST]):
        return BlockTypes.UNORDERED_LIST
    if lines_start_with_pattern(block, type_to_pattern[BlockTypes.ORDERED_LIST]):
        return BlockTypes.ORDERED_LIST
    return BlockTypes.PARAGRAPH

def lines_start_with_pattern(block, pattern):
    lines = block.split("\n")
    for line in lines:
        if not re.search(pattern, line):
            return False
    return True