from nodes.textnode import TextNode, TextType
from nodes.parentnode import ParentNode
from markdown_tools.split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from markdown_tools.extract_blocks import markdown_to_blocks, block_to_block_type, BlockTypes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockTypes.PARAGRAPH:
            children = text_to_children(block)
            node = ParentNode("p", children)
        elif block_type == BlockTypes.HEADING:
            children = text_to_children(remove_formatting(block, BlockTypes.HEADING))
            node = ParentNode(get_heading_level_tag(block), children)
        elif block_type == BlockTypes.CODE:
            children = [TextNode(remove_formatting(block, BlockTypes.CODE), TextType.CODE)]
            node = ParentNode("pre", [
                ParentNode("code", children)
            ])
        elif block_type == BlockTypes.QUOTE:
            children = text_to_children(remove_formatting(block, BlockTypes.QUOTE))
            node = ParentNode("blockquote", children)
        elif block_type == BlockTypes.UNORDERED_LIST:
            children = text_to_children(remove_formatting(block, BlockTypes.UNORDERED_LIST))
            list_items = block.split("\n")
            node = ParentNode("ul", [
                ParentNode("li", text_to_children(remove_formatting(list_item, BlockTypes.UNORDERED_LIST))) for list_item in list_items
            ])
        elif block_type == BlockTypes.ORDERED_LIST:
            children = text_to_children(remove_formatting(block, BlockTypes.ORDERED_LIST))
            list_items = block.split("\n")
            node = ParentNode("ol", [
                ParentNode("li", text_to_children(remove_formatting(list_item, BlockTypes.ORDERED_LIST))) for list_item in list_items
            ])
        nodes.append(node)
    root = ParentNode("div", nodes)
    return root

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return text_nodes

def get_heading_level_tag(block):
    header_level_to_tag = {
        1: "h1",
        2: "h2",
        3: "h3",
        4: "h4",
        5: "h5",
        6: "h6"
    }
    header_level = 0
    char = block[0]
    while char == "#":
        header_level += 1
        char = block[header_level]
    return header_level_to_tag[header_level]

def remove_formatting(text, block_type):
    if block_type == BlockTypes.HEADING:
        return text.lstrip("# ")
    if block_type == BlockTypes.CODE:
        return text.strip("`")
    if block_type == BlockTypes.QUOTE:
        lines = []
        for line in text.split("\n"):
            lines.append(line.lstrip(">"))
        return "\n".join(lines)
    if block_type == BlockTypes.ORDERED_LIST:
        lines = []
        for line in text.split("\n"):
            parts = line.split(". ")
            new_line = ".".join(parts[1:])
            lines.append(new_line)
        return "\n".join(lines)
    if block_type == BlockTypes.UNORDERED_LIST:
        lines = []
        for line in text.split("\n"):
            lines.append(line[2:])
        return "\n".join(lines)
