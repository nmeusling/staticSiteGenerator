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

    if block[0:3] == '```' and block[-3:] == '```':
        return BlockTypes.CODE
    header_pattern = r"^[#]{1,6}"
    
    return BlockTypes.PARAGRAPH