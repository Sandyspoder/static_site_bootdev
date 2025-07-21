from enum import Enum

class TextType(Enum):
	PLAIN_TEXT = "plain"
	BOLD_TEXT = "bold"
	ITALIC_TEXT = "italic"
	CODE_TEXT = "code"
	LINK_FORMAT = "link"
	IMAGE_FORMAT = "image"

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
