class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return_str = ""
        if self.props == None:
            return return_str
        for key in self.props:
            return_str += f' {key}="{self.props[key]}"'
        return return_str

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("No value found, leaf node must include a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("No tag found, parent node must include a tag")
        if not self.children:
            raise ValueError("No children found, parent node must have children")
        return f"<{self.tag}{self.props_to_html()}>{self.get_children()}</{self.tag}>"
        
    def get_children(self):
        return_str = ""
        for node in self.children:
            return_str += node.to_html()
        return return_str
        
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    