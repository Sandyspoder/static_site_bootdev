from htmlnode import *
import re
from textnode import *

def text_node_to_html_node(self):
	match self.text_type:
		case TextType.TEXT:
			return LeafNode(tag=None, value = self.text)
		case TextType.BOLD:
			return LeafNode(tag="b", value = self.text)
		case TextType.ITALIC:
			return LeafNode(tag="i", value = self.text)
		case TextType.LINK:
			return LeafNode(tag="a", value = self.text, props = "href")
		case TextType.IMAGE:
			return LeafNode(tag="img", value = "", props = ["src", "alt"])
		case _:
			raise Exception("text_type not defined")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	final_list = []
	for nodes in old_nodes:
		if nodes.text_type is not TextType.TEXT:
			final_list.append(nodes)

		else:
			match text_type:
				case TextType.BOLD:
					if not delimiter == "**":
						raise Exception("Wrong input delimiter defined for TextType.BOLD")
					new_nodes = nodes.text.split("**")
				case TextType.ITALIC:
					if not delimiter == "_":
						raise Exception("Wrong input delimiter defined for TextType.ITALIC")
					new_nodes = nodes.text.split("_")
				case TextType.CODE:
					if not delimiter == "`":
						raise Exception("Wrong input delimiter defined for TextType.CODE")
					new_nodes = nodes.text.split("`")
				case _:
					raise Exception("text_type not defined")

			newer_nodes = []
			if len(new_nodes) % 2 == 1:
				for i in range(0,len(new_nodes)-1,2):
					newer_nodes.append(TextNode(new_nodes[i],TextType.TEXT))
					newer_nodes.append(TextNode(new_nodes[i+1],text_type))
				newer_nodes.append(TextNode(new_nodes[-1],TextType.TEXT))
				final_list.extend(newer_nodes)
			else:
				raise Exception("Unmatch delimiters")
	return final_list

def extract_markdown_images(text):
	return re.findall(r"!\[(.*?)\]\((.*?)\)",text)

def extract_markdown_links(text):
	return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)",text)

def split_nodes_link(old_nodes):
	output_list = []
	for nodes in old_nodes:
		if nodes.text_type is not TextType.TEXT:
			output_list.append(nodes)
		else:
			link_nodes = extract_markdown_links(nodes.text)
			if link_nodes:
				starting_index = 0
				for i in range(0,len(link_nodes)):
					output_list.append(TextNode(nodes.text[starting_index:nodes.text.find(link_nodes[i][0],starting_index)-1],TextType.TEXT))
					output_list.append(TextNode(link_nodes[i][0],TextType.LINK,link_nodes[i][1]))
					starting_index = nodes.text.find(link_nodes[i][1],starting_index) + len(link_nodes[i][1]) + 1
				if not starting_index >= len(nodes.text):
					output_list.append(TextNode(nodes.text[starting_index:],TextType.TEXT))
			else:
				output_list.append(nodes)
	return output_list

def split_nodes_image(old_nodes):
	output_list = []
	for nodes in old_nodes:
		if nodes.text_type is not TextType.TEXT:
			output_list.append(nodes)
		else:
			image_nodes = extract_markdown_images(nodes.text)
			if image_nodes:
				starting_index = 0
				for i in range(0,len(image_nodes)):
					output_list.append(TextNode(nodes.text[starting_index:nodes.text.find(image_nodes[i][0],starting_index)-2],TextType.TEXT))
					output_list.append(TextNode(image_nodes[i][0],TextType.IMAGE,image_nodes[i][1]))
					starting_index = nodes.text.find(image_nodes[i][1],starting_index) + len(image_nodes[i][1]) + 1
				if not starting_index >= len(nodes.text):
					output_list.append(TextNode(nodes.text[starting_index:],TextType.TEXT))
			else:
				output_list.append(nodes)
	return output_list

def text_to_textnodes(text):

	return split_nodes_image(
		split_nodes_link(
			split_nodes_delimiter(
				split_nodes_delimiter(
					split_nodes_delimiter(
						text,"**",TextType.BOLD
					)
					,"_",TextType.ITALIC
				)
				,"`",TextType.CODE
			)
		)
	)

def markdown_to_blocks(markdown):
	output_list = markdown.split("\n\n")
	filtered = filter(lambda x: x is not None,output_list)
	return list(map(lambda x: x.strip(),filtered))

def block_to_block_type(block):

	if block.startswith(("# ","## ","### ","#### ","##### ","###### ")):
		return BlockType.heading
	elif block.startswith("```") and block.endswith("```"):
		return BlockType.code
	elif block.startswith(">"):
		return BlockType.quote
	elif block.startswith("- "):
		return BlockType.unordered_list
	elif block[0].isnumeric() and block[1:2] == ". ":
		return BlockType.ordered_list
	else:
		return BlockType.paragraph

	