class HTMLNode:

	def __init__(self, tag= None,value= None, children= None, props= None):

		self.tag = tag
		self.value = value
		self.children = children 
		self.props = props
    
	def to_html(self):
		raise NotImplementedError 

	def props_to_html(self):
		output_string = ""
		for value_pair in self.props.items():
			output_string += f' {value_pair[0]}="{value_pair[1]}"'
		return output_string
    
	def __repr__(self):
		print(f" tag = {self.tag}/n")
		print(f" value = {self.value}/n")
		print(f" childrent = {self.children}/n")
		print(f" props = {self.props}/n")


class LeafNode(HTMLNode):
	def __init__(self,tag, value, props= None):
		super().__init__(tag, value, props)


	def to_html(self):
		if self.value == None:
			raise ValueError
		if self.tag == None:
			return self.value
		
		if self.props == None:
			return f"<{self.tag}>{self.value}</{self.tag}>"
		
		return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
	def __init__(self,tag,children,props = None):
		super().__init__(tag=tag,children=children,props=props)

	def to_html(self):
		if self.tag == None:
			raise ValueError("Tag not identifyable")
		if not self.children:
			raise ValueError("Child not identifyable")

		starting_string = f'<{self.tag}>'
		for child in self.children:
			starting_string += child.to_html()
		return starting_string + f'</{self.tag}>'
		