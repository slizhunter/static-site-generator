import re

from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = [s.strip() for s in blocks]
    new_blocks = []
    for block in stripped_blocks:
        if block != "":
            new_blocks.append(block)
    return new_blocks

def block_to_blocktype(block):
    lines = block.split("\n")
    if re.findall(r"^(#){1,6}(?= )", block, re.MULTILINE):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    elif len(lines) == 1 and lines[0].startswith("```") and lines[0].endswith("```"):
        return BlockType.CODE
    if re.match(r"\A>.*(?:\n>.*)*\Z", block):
        return BlockType.QUOTE
    if re.match(r"\A- .*(?:\n- .*)*\Z", block):
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children_nodes = []
    for block in blocks:
        node = block_to_htmlnode(block)
        children_nodes.append(node)
    return ParentNode("div", children_nodes)

def block_to_htmlnode(block):
    block_type = block_to_blocktype(block)
    if block_type is BlockType.PARAGRAPH:
        return ParentNode("p", text_to_children(block.replace('\n', ' ')))
    if block_type is BlockType.HEADING:
        match = re.search(r"^(#{1,6})(?= )", block, re.MULTILINE)
        i = len(match.group(1))
        return ParentNode(f"h{i}", text_to_children(block[(i+1):]))
    if block_type is BlockType.CODE:
        return ParentNode("pre", [ParentNode("code", [text_node_to_html_node(TextNode(block[4:-3], TextType.TEXT))])])
    if block_type is BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type is BlockType.UNORDERED_LIST:
        return list_to_html_node(block, block_type)
    if block_type is BlockType.ORDERED_LIST:
        return list_to_html_node(block, block_type)
    raise ValueError("Invalid block type")

def quote_to_html_node(block):
    new_lines = ""
    lines = block.split("\n")
    for line in lines:
        new_lines += (line[1:] + " ")
    return ParentNode("blockquote", text_to_children(new_lines.strip()))

def list_to_html_node(block, list_type):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        space_index = line.find(" ")
        li_nodes.append(ParentNode("li", text_to_children(line[space_index + 1:])))
    if list_type == BlockType.ORDERED_LIST:
        return ParentNode("ol", li_nodes)
    elif list_type == BlockType.UNORDERED_LIST:
        return ParentNode("ul", li_nodes)

def text_to_children(text):
    text_nodes = text_to_textnodes(text) #text_nodes is a LIST of TextNodes, with TextType and URLs
    html_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node) #html_node is a LeafNode
        html_nodes.append(html_node)
    return html_nodes

def extract_title(markdown):
    md_blocks = markdown_to_blocks(markdown)
    for block in md_blocks:
        if block_to_blocktype(block) == BlockType.HEADING:
            match = re.search(r"^(#{1})(?= )", block)
            if match:
                return block[2:]