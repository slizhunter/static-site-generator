import unittest

from block_markdown import (
    markdown_to_blocks,
    markdown_to_html_node,
    block_to_blocktype, 
    BlockType
)

class TestInlineMarkdown(unittest.TestCase):

    def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
    
    def test_markdown_to_blocks_extra_newlines(self):
            md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items



"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

    def test_markdown_to_no_blocks(self):
            md = """
This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n- This is a list\n- with items",
                ],
            )

    def test_markdown_to_blocks_empty(self):
            md = ""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [],
            )
    
    #BLOCK TO BLOCKTYPE TESTS

    def test_blocktype_heading(self):
           block = "# This is a heading"
           block_type = block_to_blocktype(block)
           self.assertEqual(
                block_type,
                BlockType.HEADING,
            )
    
    def test_blocktype_bad_heading(self):
           block = "#This is a bad heading"
           block_type = block_to_blocktype(block)
           self.assertNotEqual(
                block_type,
                BlockType.HEADING,
            )
    
    def test_blocktype_code(self):
           block = "```This is a code block```"
           block_type = block_to_blocktype(block)
           self.assertEqual(
                block_type,
                BlockType.CODE,
            )

    def test_blocktype_multiline_code(self):
           block = '''```
This is a code block
```'''
           block_type = block_to_blocktype(block)
           self.assertEqual(
                block_type,
                BlockType.CODE,
            )       
           
    def test_blocktype_bad_code(self):
           block = "```This is a bad code block"
           block_type = block_to_blocktype(block)
           self.assertNotEqual(
                block_type,
                BlockType.CODE,
            )
    
    def test_blocktype_quote(self):
           block = ">This is a quote"
           block_type = block_to_blocktype(block)
           self.assertEqual(
                block_type,
                BlockType.QUOTE,
            )
    
    def test_blocktype_multi_quote(self):
           block = '''>This is a quote
>More quoting
>Even more quote
>So much quotage'''
           block_type = block_to_blocktype(block)
           self.assertEqual(
                block_type,
                BlockType.QUOTE,
            )
    
    def test_blocktype_bad_quote(self):
           block = '''>This is a quote
>More quoting
Not a quote?
>So much quotage'''
           block_type = block_to_blocktype(block)
           self.assertNotEqual(
                block_type,
                BlockType.QUOTE,
            )
           
    def test_blocktype_unordered_list(self):
           block = "- This is an unordered list"
           block_type = block_to_blocktype(block)
           self.assertEqual(
                block_type,
                BlockType.UNORDERED_LIST,
            )
           
    def test_blocktype_multi_unordered_list(self):
           block = '''- This is an unordered list
- More list
- Lots of things
- Wow, much list'''
           block_type = block_to_blocktype(block)
           self.assertEqual(
                block_type,
                BlockType.UNORDERED_LIST,
            )
    
    def test_blocktype_bad_unordered_list(self):
           block = "-This is not an unordered list"
           block_type = block_to_blocktype(block)
           self.assertNotEqual(
                block_type,
                BlockType.UNORDERED_LIST,
            )
    
    def test_blocktype_bad_multi_unordered_list(self):
           block = '''- This is an unordered list
- More list
-Oops, bad list
- Wow, much list'''
           block_type = block_to_blocktype(block)
           self.assertNotEqual(
                block_type,
                BlockType.UNORDERED_LIST,
            )
           
    def test_blocktype_ordered_list(self):
           block = '''1. This is an ordered list
2. This is the second line of the list
3. This is the third line of the list
4. Fourth
5. Fifth
6. Sixth
7. Um
8. So
9. Long
10. Thanks
11. For all the list'''
           block_type = block_to_blocktype(block)
           self.assertEqual(
                block_type,
                BlockType.ORDERED_LIST,
            )
           
    def test_blocktype_bad_ordered_list(self):
           block = '''1. This is an ordered list
2. This is the second line of the list
4. This is the third line of the list'''
           block_type = block_to_blocktype(block)
           self.assertNotEqual(
                block_type,
                BlockType.ORDERED_LIST,
            )       
    
    def test_blocktype_bad_ordered_list_2(self):
           block = '''10. This is an ordered list, starting at 10?
11. This is the second line of the list
12. This is the third line of the list'''
           block_type = block_to_blocktype(block)
           self.assertNotEqual(
                block_type,
                BlockType.ORDERED_LIST,
            )
           
    def test_blocktype_paragraph(self):
           block = "This is a normal paragraph"
           block_type = block_to_blocktype(block)
           self.assertEqual(
                block_type,
                BlockType.PARAGRAPH,
            )

#MARKDOWN TO HTMLNODE TESTS

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
## This is an H2 Heading

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This is an H2 Heading</h2><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_quotes(self):
        md = """
## This is an H2 Heading

>This is a direct quote
>An actual, direct quote

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This is an H2 Heading</h2><blockquote>This is a direct quote An actual, direct quote</blockquote><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_unordered_list(self):
        md = """
- This is an unordered list
- There are many like it
- But this one is mine

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is an unordered list</li><li>There are many like it</li><li>But this one is mine</li></ul></div>",
        )
    
    def test_bad_unordered_list(self):
        md = """
- This is a baaaaad unordered list
There are many like it
- But this one is mine

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertNotEqual(
            html,
            "<div><ul><li>This is a baaaaad unordered list</li><li>There are many like it</li><li>But this one is mine</li></ul></div>",
        )
    
    def test_ordered_list(self):
        md = """
1. This is an ordered list
2. There are many like it
3. But this one is mine

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an ordered list</li><li>There are many like it</li><li>But this one is mine</li></ol></div>",
        )

    def test_bad_ordered_list(self):
        md = """
1. This is an ordered list
5. There are many like it
3. But this one is mine

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertNotEqual(
            html,
            "<div><ol><li>This is an ordered list</li><li>There are many like it</li><li>But this one is mine</li></ol></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()