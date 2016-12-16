
class node(object):
	"""docstring for node"""
	def __init__(self, word, pos):
		super(node, self).__init__()
		self.word = word
		self.pos = pos
		self.force = False
		self.g = 0.0
		self.h = 0.0
		
