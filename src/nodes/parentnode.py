from nodes.htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node must have a tag")
        if not self.children:
            raise ValueError("Parent node must have at least one child")
        props = self.props_to_html()
        if props: 
            props = f" {props}"
        html_open = f'<{self.tag}{props}>'
        html_close = f'</{self.tag}>'
        child_html = ""
        for child in self.children:
            child_html = f"{child_html}{child.to_html()}"
        return f"{html_open}{child_html}{html_close}"
