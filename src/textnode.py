from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE_TEXT = 'code_text'
    LINK = 'link'
    IMAGE = 'image'

class TextNode:

    def __init__(self, text : str, text_type: TextType, url : str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'

def text_node_to_html_node(text_node):
    if isinstance(text_node, TextNode) and isinstance(text_node.text_type, TextType):
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(tag=None, value=text_node.text)
            case TextType.BOLD:
                return LeafNode(tag='b', value=text_node.text)
            case TextType.ITALIC:
                return LeafNode(tag='i', value=text_node.text)
            case TextType.CODE_TEXT:
                return LeafNode(tag='code', value=text_node.text)
            case TextType.LINK:
                return LeafNode(tag='a', value=text_node.text, props={"href": text_node.url})
            case TextType.IMAGE:
                return LeafNode(tag='img', value="", props={'alt': text_node.text, 'src' : text_node.url})
    else:
        raise Exception('input is not type of TextNode')