from textnode import TextType, TextNode




def split_nodes_delimiter(old_nodes, delimiter, text_type):
    delimiters = {
        "**": TextType.BOLD,
        "*": TextType.ITALIC,
        "`": TextType.CODE,
    }

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) == 1:
            new_nodes.append(node)
            continue
        if len(parts) %2 == 0:
            raise(ValueError(f"Invalid markdown syntax. Delimiter {delimiter} does not close in {node.text}"))

        for i in range (0, len(parts)):
            if len(parts[i])==0:
                continue
            if i%2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.NORMAL))
            else:
                new_nodes.append(TextNode(parts[i], delimiters[delimiter]))
    return new_nodes

def extract_markdown_images(text):
    alt_text = ""
    url = ""

    return alt_text, url    