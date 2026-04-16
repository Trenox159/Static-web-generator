import re
from textnode import TextNode, TextType, text_node_to_html_node
from blocknode import block_to_block_type, BlockType
from htmlnode import ParentNode, LeafNode, HTMLNode
import os

def split_nodes_delimiter(old_nodes : TextNode, delimiter : str, text_type : TextType):
    result = []
    for old_node in old_nodes:
        
        if old_node.text_type is not TextType.TEXT:
            result.append(old_node)
            continue

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
                result.append(TextNode(text, text_type))

    return result

def extract_markdown_images(text : str):
    extracted_groups = re.findall(r'\!\[(.*?)\]\((.*?)\)', text)
    return extracted_groups

def extract_markdown_links(text : str):
    extracted_groups = re.findall(r'\[(.*?)\]\((.*?)\)',text)
    return extracted_groups

def split_nodes_image(old_nodes :list[TextNode]):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        text = old_node.text
        extracted_groups = extract_markdown_images(text)
        
        for extracted_group in extracted_groups:
            section = text.split(f'![{extracted_group[0]}]({extracted_group[1]})', 1)
            result.append(TextNode(section[0], TextType.TEXT))
            result.append(TextNode(extracted_group[0], TextType.IMAGE, extracted_group[1]))
            text = section[-1]
        if text:
            result.append(TextNode(text, TextType.TEXT))
    return result

def split_nodes_links(old_nodes : list[TextNode]):
    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        text = old_node.text
        extracted_groups = extract_markdown_links(text)
        
        for extracted_group in extracted_groups:
            section = text.split(f'[{extracted_group[0]}]({extracted_group[1]})', 1)
            result.append(TextNode(section[0], TextType.TEXT))
            result.append(TextNode(extracted_group[0], TextType.LINK, extracted_group[1]))
            text = section[-1]
        if text:
            result.append(TextNode(text, TextType.TEXT))
    return result

def text_to_textnodes(text : str):
    result = split_nodes_image([TextNode(text, TextType.TEXT)])
    result = split_nodes_links(result)
    result = split_nodes_delimiter(result, '**', TextType.BOLD)
    result = split_nodes_delimiter(result, '_', TextType.ITALIC)  
    result = split_nodes_delimiter(result, '`', TextType.CODE_TEXT)
    

    return result

def markdown_to_blocks(markdown: str):
    result = markdown.split('\n\n')
    result = list(map(lambda x : x.strip(), result))
    result = [el for el in result if el]
    return result

def convert_text_nodes_to_html(text_nodes : list[TextNode]):
    result = []
    for text_node in text_nodes:
        result.append(text_node_to_html_node(text_node))

    return result

def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    rootNode = ParentNode('div', [], None)
    for block in blocks:
        type_of_block = block_to_block_type(block)
        match type_of_block:
            case BlockType.PARAGRAPH:
                parentBlock = ParentNode('p', [])
                block_value = block.replace('\n', ' ')
                textnode = text_to_textnodes(block_value)
                parentBlock.children.extend(convert_text_nodes_to_html(textnode))
            case BlockType.QUOTE:
                parentBlock = ParentNode('blockquote', [])
                block_value = block.replace('\n', ' ').replace('>', '').strip()
                textnode = text_to_textnodes(block_value)
                parentBlock.children.extend(convert_text_nodes_to_html(textnode))
            case BlockType.UNORD_LIST:
                parentBlock = ParentNode('ul', [])
                for line in block.split('\n'):
                    textNodes = text_to_textnodes(line[2:])
                    htmlNodes = convert_text_nodes_to_html(textNodes)
                    node = ParentNode('li', htmlNodes)
                    parentBlock.children.append(node)
            case BlockType.ORD_LIST:
                parentBlock = ParentNode('ol', [])
                for line in block.split('\n'):
                    textNodes = text_to_textnodes(line[line.find(' ')+1:])
                    htmlNodes = convert_text_nodes_to_html(textNodes)
                    node = ParentNode('li', htmlNodes)
                    parentBlock.children.append(node)
            case BlockType.CODE:
                parentBlock = ParentNode('pre', [LeafNode('code', block.replace('```\n','').replace('```', ''))])
            case BlockType.HEADING:
                reResult = re.match(r'^#{1,6}(?!#)', block)
                headingLevel = len(reResult.group())
                parentBlock = LeafNode(f'h{headingLevel}', block.replace('#', '').strip())

        rootNode.children.append(parentBlock)
    
    return rootNode
        
def extract_title(markdown):
    regex = re.compile(r'^# (.*)', flags=re.MULTILINE | re.UNICODE)
    matches = regex.findall(markdown)
    return matches[0]

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    with open(from_path, 'r') as file:
        content_from_path = file.read()

    with open(template_path, 'r') as file:
        content_template_path = file.read()
    
    html = markdown_to_html_node(content_from_path).to_html()
    #print(html)

    title = extract_title(content_from_path)
    
    content_template_path = content_template_path.replace(r'{{ Title }}', title).replace(r'{{ Content }}', html)

    with open(dest_path, 'w') as file:
        file.write(content_template_path)


md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

md = """
This is **bolded** paragraph
text in a p
tag here


1. line 1
2. line 2
3. line 3 

"""

md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""


#print(repr(markdown_to_html_node(md).to_html()))