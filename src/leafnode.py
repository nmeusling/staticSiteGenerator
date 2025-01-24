from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props =None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node must have a value")
        if self.tag is None:
            return self.value

        props = self.props_to_html()
        if props:
            props = f" {props}"
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
        
