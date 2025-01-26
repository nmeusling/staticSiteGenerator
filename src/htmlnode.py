class HTMLNode ():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        props = ""
        if not self.props:
            return props
        for key, value in self.props.items():
            props = f'{props} {key}="{value}"'
        return props[1:]

    def __repr__(self):
        return f"Tag: {self.tag}\nValue: {self.value}\nChildren: \n\n{self.children}\n\nProps: {self.props}"

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
