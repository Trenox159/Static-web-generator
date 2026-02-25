

class HTMLNode:

    def __init__(self, tag : str = None, value : str = None, children : list = [], props : dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError('function is not implemented')

    def props_to_html(self):
        if not self.props:
            return ''
        result = []
        for prop in self.props:
            result.append(f' {prop}="{self.props[prop]}"')

        return "".join(result)

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class LeafNode(HTMLNode):

    def __init__(self, tag : str, value : str , props : dict[str, str] | None = None):
        super().__init__(tag, value, [], props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError('All leaf nodes must have value')
        if not self.tag:
            return f'{self.value}'

        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.props})'

class ParentNode(HTMLNode):
    def __init__(self, tag : str, children : list[HTMLNode], props : dict[str, str] | None = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError('Node can not be without tag')
        if not self.children:
            raise ValueError('Parent node can not be without children value')
        
        result = []
        result.append(f'<{self.tag}>')
        for child in self.children:
            result.append(child.to_html())
        result.append(f'</{self.tag}>')

        return ''.join(result)