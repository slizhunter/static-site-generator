import re

from textnode import TextNode, TextType

#node = TextNode("This is text with a `code block` word", TextType.TEXT)
#new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
#return = 
#[
#    TextNode("This is text with a ", TextType.TEXT),
#    TextNode("code block", TextType.CODE),
#    TextNode(" word", TextType.TEXT),
#]
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        split_node_text = node.text.split(delimiter)
        if len(split_node_text) % 2 == 0:
            raise Exception(f"Invalid Markdown syntax: no matching closing delimiter for '{delimiter}'")
        for i in range(len(split_node_text)):
            if split_node_text[i] == '':
                continue
            new_list.append(TextNode(split_node_text[i], TextType.TEXT if i % 2 == 0 else text_type))
    return new_list

def split_nodes_image(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        image_text = extract_markdown_images(node.text)
        current_text_to_process = node.text
        for image in image_text:
            split_node_text = current_text_to_process.split(f"![{image[0]}]({image[1]})", 1)
            if split_node_text[0] == '':
                new_list.append(TextNode(image[0], TextType.IMAGE, image[1]))
            else:
                new_list.append(TextNode(split_node_text[0], TextType.TEXT))
                new_list.append(TextNode(image[0], TextType.IMAGE, image[1]))
            current_text_to_process = split_node_text[1]
        if current_text_to_process != "":
            new_list.append(TextNode(current_text_to_process, TextType.TEXT))
    return new_list

def split_nodes_link(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        link_text = extract_markdown_links(node.text)
        current_text_to_process = node.text
        for link in link_text:
            split_node_text = current_text_to_process.split(f"[{link[0]}]({link[1]})", 1)
            if split_node_text[0] == '':
                new_list.append(TextNode(link[0], TextType.LINK, link[1]))
            else:
                new_list.append(TextNode(split_node_text[0], TextType.TEXT))
                new_list.append(TextNode(link[0], TextType.LINK, link[1]))
            current_text_to_process = split_node_text[1]
        if current_text_to_process != "":
            new_list.append(TextNode(current_text_to_process, TextType.TEXT))
    return new_list

def text_to_textnodes(text):
    text_node = [TextNode(text, TextType.TEXT)]
    text_node = split_nodes_delimiter(text_node, "**", TextType.BOLD)
    text_node = split_nodes_delimiter(text_node, "_", TextType.ITALIC)
    text_node = split_nodes_delimiter(text_node, "`", TextType.CODE)
    text_node = split_nodes_image(text_node)
    text_node = split_nodes_link(text_node)
    return text_node

#text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
#print(extract_markdown_images(text))
# [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

#text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
#print(extract_markdown_links(text))
# [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

