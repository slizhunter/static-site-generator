import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "google.com")
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "apple.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "google.com")
        self.assertNotEqual(node, node2)

        #TEXTNODE TO HTMLNODE TESTS

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_bold_node = text_node_to_html_node(node)
        self.assertEqual(html_bold_node.tag, "b")
        self.assertEqual(html_bold_node.value, "This is a bold node")

    def test_text_link(self):
        node = TextNode("This is a link", TextType.LINK, "www.google.com")
        html_link_node = text_node_to_html_node(node)
        self.assertEqual(html_link_node.tag, "a")
        self.assertEqual(html_link_node.value, "This is a link")
        self.assertEqual(html_link_node.props, {"href": "www.google.com"})

    def test_text_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_link_node = text_node_to_html_node(node)
        self.assertEqual(html_link_node.tag, "img")
        self.assertEqual(html_link_node.value, None)
        self.assertEqual(
            html_link_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_wrong_text_type(self):
        text_type = "GOOFY"
        node = TextNode("This is a text node", text_type)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()