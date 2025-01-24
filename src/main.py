from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    text = TextNode("this is sample text", TextType.BOLD, "www.google.com")
    print(text)
    text2 = TextNode("this is more sample", TextType.ITALIC)
    print(text2)
    grandchild = HTMLNode("a", "1232")
    child = HTMLNode("p", "123", children=[grandchild])
    html = HTMLNode("a", "test", children=[child], props={"ab": "def", "df": "dsfs"})
    print(html)
    print(html.props_to_html())

if __name__ == "__main__":
    main()