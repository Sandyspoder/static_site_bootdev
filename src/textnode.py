from enum import Enum
from htmlnode import *

class TextType(Enum):
	TEXT = "text"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

BlockType = Enum("BlockType",["paragraph","heading","code","quote","unordered_list","ordered_list"])

class TextNode:

	def __init__(self, text ,text_type ,url = None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self,other):
		if (self.text == other.text and 
			self.text_type == other.text_type and 
			self.url == other.url
		):
			return True

	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type}, {self.url})"