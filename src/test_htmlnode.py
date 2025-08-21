import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple_attributes(self):
        node = HTMLNode(
            "a",
            "Click me",
            None,
            {"href": "https://www.example.com", "target": "_blank", "class": "link"}
        )
        # Should have leading space and proper formatting
        expected = ' href="https://www.example.com" target="_blank" class="link"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_single_attribute(self):
        node = HTMLNode("p", "Hello", None, {"class": "greeting"})
        self.assertEqual(node.props_to_html(), ' class="greeting"')

    def test_props_to_html_empty_props(self):
        node = HTMLNode("div", "Content", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none_props(self):
        node = HTMLNode("span", "Text")
        self.assertEqual(node.props_to_html(), "")

    def test_constructor_all_parameters(self):
        children = [HTMLNode("span", "child")]
        props = {"id": "main", "class": "container"}
        node = HTMLNode("div", "parent", children, props)
        
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "parent")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_constructor_defaults_to_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_to_html_raises_not_implemented(self):
        node = HTMLNode("p", "test")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr_with_all_fields(self):
        node = HTMLNode("h1", "Title", None, {"class": "header"})
        expected = "HTMLNode(h1, Title, children: None, {'class': 'header'})"
        self.assertEqual(repr(node), expected)

    def test_repr_with_children(self):
        child = HTMLNode("span", "child text")
        node = HTMLNode("div", None, [child], {"id": "parent"})
        expected = f"HTMLNode(div, None, children: [{repr(child)}], {{'id': 'parent'}})"
        self.assertEqual(repr(node), expected)

    # LEAF NODES TESTS

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some raw text.")
        self.assertEqual(node.to_html(), "Just some raw text.")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "This is a div.")
        self.assertEqual(node.to_html(), "<div>This is a div.</div>")

    def test_leaf_to_html_empty_value_raises_error(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    #PARENT NODE TESTS

    def test_to_html_with_multiple_children(self):
        children_nodes = [
                            LeafNode("b", "Bold text"),
                            LeafNode(None, "Normal text"),
                            LeafNode("i", "italic text"),
                            LeafNode(None, "Normal text"),
                         ]
        parent_node = ParentNode("p", children_nodes)
        self.assertEqual(parent_node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_with_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_with_empty_children_list(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_mixed_children(self):
        leaf_child = LeafNode("span", "leaf")
        parent_child = ParentNode("div", [LeafNode("b", "nested")])
        parent_node = ParentNode("section", [leaf_child, parent_child])
        self.assertEqual(
            parent_node.to_html(),
            "<section><span>leaf</span><div><b>nested</b></div></section>"
        )

    def test_to_html_with_deep_nesting(self):
        grandchild_node = LeafNode("b", "grandchild")
        deep_nested_node = ParentNode("span", [grandchild_node])
        nested_node = ParentNode("section", [deep_nested_node])
        child_node = ParentNode("span", [nested_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><section><span><b>grandchild</b></span></section></span></div>"
        )
    
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>'
        )

if __name__ == "__main__":
    unittest.main()