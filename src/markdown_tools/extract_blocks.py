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
        BlockTypes.CODE: r"^```.*```$",
        BlockTypes.HEADING: r"^[#]{1,6} "
    }
    if re.search(type_to_pattern[BlockTypes.HEADING], block):
        return BlockTypes.HEADING
    if re.search(type_to_pattern[BlockTypes.CODE], block):
        return BlockTypes.CODE
    lines = split(block, "\n")
    
    type_to_start_char = {
        BlockTypes.QUOTE:  ">",
        BlockTypes.UNORDERED_LIST: ""
    }
    is_quote = True
    for line in lines:
        if line[0] != ">":
            is_quote = False
            break

    if is_quote:
        return BlockTypes.QUOTE

    is_unordered_list = True
    for line in lines:
        if line
    
    return BlockTypes.PARAGRAPH