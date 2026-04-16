from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORD_LIST = 'unord_list'
    ORD_LIST = 'ord_list'


def block_to_block_type(blocknode : str):

    if bool(re.match(r'^#{1,6}(?!#)', blocknode)):
        return BlockType.HEADING
    if bool(re.match(r'^```.*?```$', blocknode, re.DOTALL)):
        return BlockType.CODE
    if blocknode.startswith('>'):
        hasQuoteBlock = True
        for line in blocknode.split('\n'):
            if not line.startswith('>'):
               hasQuoteBlock = False  
               break
        
        if hasQuoteBlock:
            return BlockType.QUOTE
    
    if blocknode.startswith('- '):
        hasUnordList = True
        for line in blocknode.split('\n'):
            if not line.startswith('- '):
                hasUnordList = False
                break
        
        if hasUnordList:
            return BlockType.UNORD_LIST
    
    if blocknode.startswith('1. '):
        increment = 1 
        hasOrderList = True
        for line in blocknode.split('\n'):
            if not line.startswith(f'{increment}.'):
                hasOrderList = False
                break
            else:
                increment += 1
        
        if hasOrderList:
            return BlockType.ORD_LIST
    
    return BlockType.PARAGRAPH
            
            