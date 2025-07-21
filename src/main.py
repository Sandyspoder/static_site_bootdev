from textnode import TextNode, TextType

def main():
	textnode = TextNode("This is some anchor text", "link")
	print(textnode.__repr__())
main()