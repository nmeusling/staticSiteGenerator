from textnode import TextNode, TextType

def main():
    text = TextNode("this is sample text", TextType.BOLD, "www.google.com")
    print(text)
    text2 = TextNode("this is more sample", TextType.ITALIC)
    print(text2)

if __name__ == "__main__":
    main()