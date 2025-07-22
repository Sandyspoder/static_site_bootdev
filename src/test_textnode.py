import unittest
from enum import Enum
from textnode import *
from functs_file import *

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

	def test_split_nodes_delimiter_1(self):
		node = TextNode("This is text with a `code block` word", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

		new_nodes_expected = [
    		TextNode("This is text with a ", TextType.TEXT),
    		TextNode("code block", TextType.CODE),
    		TextNode(" word", TextType.TEXT),
		]
		self.assertEqual(new_nodes,new_nodes_expected)


	def test_split_nodes_delimiter_wrong_type(self):
		try:
			node = TextNode("This is text with a `code block` word", TextType.TEXT)
			new_nodes = split_nodes_delimiter([node], "**", TextType.CODE)
		except Exception as e:
			print(f"caught error :{e}")

	def test_extract_markdown_images(self):
		matches = extract_markdown_images(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
		)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
	def test_extract_markdown_images(self):
		matches = extract_markdown_images(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
		)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
	def test_split_link(self):
		node = TextNode(
			"This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and another ", TextType.TEXT),
				TextNode(
					"second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
				),
			],
			new_nodes,
		)
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
	def test_text_to_textnodes(self):
		text_node = [TextNode(f"This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",TextType.TEXT)]
		converted_text = text_to_textnodes(text_node)
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
			converted_text,
		)

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

	def test_block_to_block_type(self):

		test_string = block_to_block_type("## ")

		self.assertListEqual(test_string,BlockType.heading)

if __name__ == "__main__":
	unittest.main()
