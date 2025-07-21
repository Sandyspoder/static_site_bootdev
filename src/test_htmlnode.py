import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
	def test_eq(self):
		node = HTMLNode(tag = "tag", value = "value")
		node2 = HTMLNode(tag = "tag", value = "value")
		self.assertEqual(node , node)

	def test_no_input(self):
		node = HTMLNode()
		self.assertTrue(node.tag == None)
		self.assertTrue(node.value == None)
		self.assertTrue(node.children == None)
		self.assertTrue(node.props == None)

	def test_props_to_html(self):
		node = HTMLNode(props = {"href": "https://www.google.com","target": "_blank",})
		method_val = node.props_to_html()
		specified_val = f' href="https://www.google.com" target="_blank"'
		self.assertEqual(method_val, specified_val)

	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

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

if __name__ == "__main__":
	unittest.main()
