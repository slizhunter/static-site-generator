import shutil
import os
import sys

from pathlib import Path
from textnode import TextNode, TextType
from block_markdown import (
    extract_title,
    markdown_to_html_node
)

def prepare_directory(directory):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    dir_to_prepare = os.path.join(parent_dir, directory)

    if os.path.exists(dir_to_prepare):
        print(f"Deleting {dir_to_prepare}!")
        shutil.rmtree(dir_to_prepare)
        os.mkdir(dir_to_prepare)
        print(f"{dir_to_prepare} created!")
    else:
        print(f"{dir_to_prepare} does not exist!")
        os.mkdir(dir_to_prepare)
        print(f"{dir_to_prepare} created!")

def copy_directory(directory_src, directory_dst):
    print(f"Source dir: {directory_src}")
    print(f"Destination dir: {directory_dst}")
    if not os.path.exists(directory_dst):
        print(f"{directory_dst} doesn't exist, creating...")
        os.mkdir(directory_dst)
        print(f"{directory_dst} created!")

    for item in os.listdir(directory_src):
        print(f"Source item: {item}")
        src_item = os.path.join(directory_src, item)
        dst_item = os.path.join(directory_dst, item)
        if os.path.isfile(src_item):
            shutil.copy(src_item, dst_item)
            print(f"{item} copied!")
        elif os.path.isdir(src_item):
            print(f"{item} is dir, recursing...")
            copy_directory(src_item, dst_item)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    with open(from_path, 'r') as md_file:
        markdown = md_file.read()
    with open(template_path, 'r') as temp_file:
        template = temp_file.read()
    html_str = markdown_to_html_node(markdown).to_html()
    page_title = extract_title(markdown)
    template = template.replace("{{ Title }}", page_title)
    template = template.replace("{{ Content }}", html_str)
    with open(dest_path, "w") as html_file:
        html_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        print(f"Content item: {item}")
        src_item = os.path.join(dir_path_content, item)
        dst_item = os.path.join(dest_dir_path, item)
        if os.path.isfile(src_item):
            dest_path = Path(dst_item).with_suffix(".html")
            generate_page(src_item, template_path, dest_path)
        elif os.path.isdir(src_item):
            copy_directory(src_item, dst_item)
            generate_pages_recursive(src_item, template_path, dst_item)