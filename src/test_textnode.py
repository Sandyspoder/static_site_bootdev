import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_url(self):
		node = TextNode("This is a text node", TextType.BOLD)
		self.assertTrue(node.url == None)

	def test_text_type(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.TEXT)
		self.assertNotEqual(node.text_type,node2.text_type)
		
	def test_text(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")
	
	def test_bold(self):
		node = TextNode("This is a Bold node", TextType.BOLD)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "b")
		self.assertEqual(html_node.value, "This is a Bold node")

	def test_none_type(self):
		try:
			node = TextNode("This is a text node", TextType.TIMES_NEW_ROMAN)
			html_node = text_node_to_html_node(node)
			self.assertEqual(html_node.tag, None)
			self.assertEqual(html_node.value, "This is a text node")
		except Exception as e:
			print(f"caught error :{e}")


if __name__ == "__main__":
	unittest.main()
