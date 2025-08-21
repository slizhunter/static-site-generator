import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter, 
    split_nodes_image, 
    split_nodes_link, 
    extract_markdown_images, 
    extract_markdown_links, 
    text_to_textnodes
)

class TestInlineMarkdown(unittest.TestCase):
#SPLIT NODES DELIMITER TESTS

    def test_simple_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )
    
    def test_double_split(self):
        node = TextNode("This is text with a **bold** word, and another **one**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word, and another ", TextType.TEXT),
                TextNode("one", TextType.BOLD),
            ]
        )

    def test_no_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [TextNode("This is text with a `code block` word", TextType.TEXT)]
        )
    
    def test_not_text_type(self):
        node = TextNode("**This is already bold text**", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [TextNode("**This is already bold text**", TextType.BOLD)]
        )

    def test_all_delimited(self):
        node = TextNode("**This is already bold text**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [TextNode("This is already bold text", TextType.BOLD)]
        )
    
    def test_empty_delimiter(self):
        node = TextNode("This: `` is an empty code block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This: ", TextType.TEXT),
                TextNode(" is an empty code block", TextType.TEXT)
            ]
        )
    
    def test_two_delimiter_type(self):
        node = TextNode("This is text with a **bold** word, and an _italic_ one", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a **bold** word, and an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" one", TextType.TEXT),
            ]
        )
    
    def test_delimit_start(self):
        node = TextNode("_This_ is text that starts with an italic word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This", TextType.ITALIC),
                TextNode(" is text that starts with an italic word", TextType.TEXT),
            ]
        )
    
    def test_delimit_end(self):
        node = TextNode("This is text that ends with an italic _word_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text that ends with an italic ", TextType.TEXT),
                TextNode("word", TextType.ITALIC),
            ]
        )

    def test_mismatch_delimiter(self):
        node = TextNode("This is text with a **bold** word and another **one", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)
    
    #EXTRACTION TESTS

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_malformed_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev/test/Programming_(python)) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
    
    def test_extract_malformed_image_text(self):
        matches = extract_markdown_images(
            "This is text with ![nested image [brackets]](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    #SPLIT IMAGES TESTS

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_image_at_end(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) Image at start of text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" Image at start of text", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_image_only(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    
    def test_split_double_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_double_image_with_surrounding_text(self):
        node = TextNode(
            "Before ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png) After",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" After", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_no_image(self):
        node = TextNode("No images here!", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("No images here!", TextType.TEXT)],
            new_nodes
        )

    def test_non_text(self):
        node = TextNode("not text", TextType.IMAGE, "fake")
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [node],
            new_nodes
        )

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("![image](https://i.imgur.com/zjjcJKZ.png) and ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            TextNode("not text", TextType.LINK, "example.com")
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("not text", TextType.LINK, "example.com")
            ],
            new_nodes,
        )

    #SPLIT LINKS TESTS

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and another [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )
    
    def test_split_link_at_end(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) Link at start of text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" Link at start of text", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_link_only(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )
    
    def test_split_double_link(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )
    
    def test_split_double_link_with_surrounding_text(self):
        node = TextNode(
            "Before [to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev) After",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode(" After", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_no_link(self):
        node = TextNode("No links here!", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("No links here!", TextType.TEXT)],
            new_nodes
        )

    def test_non_text(self):
        node = TextNode("not text", TextType.IMAGE, "fake")
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [node],
            new_nodes
        )

    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode("[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT),
            TextNode("not text", TextType.LINK, "example.com")
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode("not text", TextType.LINK, "example.com")
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_nodes
        )

    def test_text_to_textnodes_partial(self):
        text = "This is **text** with a `code block` and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_nodes
        )
    
    def test_text_to_textnodes_empty(self):
        text = ""
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [],
            text_nodes
        )
    
    def test_text_to_textnodes_just_text(self):
        text = "This is just text"
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is just text", TextType.TEXT),
            ],
            text_nodes
        )
    
    def test_text_to_textnodes_just_bold(self):
        text = "**This is bold text**"
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is bold text", TextType.BOLD),
            ],
            text_nodes
        )

if __name__ == "__main__":
    unittest.main()