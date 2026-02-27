

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes : TextNode, delimiter : str, text_type : TextType):
    result = []
    for old_node in old_nodes:
        
        if old_node.text_type is not TextType.TEXT:
            result.append(old_node)
            continue

        match delimiter:
            case '*':
                new_type = TextType.BOLD
            case '`':
                new_type = TextType.CODE_TEXT
            case '_':
                new_type = TextType.ITALIC
            case _:
                raise Exception('invalid delimiter')

        text = old_node.text
        text = text.split(delimiter)
        if len(text) % 2 == 0:
            raise Exception('invalid markdown syntax')
        
        for idx, text in enumerate(text):
            if not text:
                continue

            if idx % 2 == 0:
                result.append(TextNode(text, TextType.TEXT))
            else:
                result.append(TextNode(text, new_type))

    return result
        

node = TextNode("This is text with a `code block` word", TextType.TEXT)
new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)