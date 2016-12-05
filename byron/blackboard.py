import nltk
from byron.pool_of_ideas import pool_of_ideas
from byron.experts.analyzing_expert import analyzing_expert

class blackboard(object):
	"""docstring for blackboard"""
	def __init__(self,inspiration):
		super(blackboard, self).__init__()
		self.inspiration = self.process_input(inspiration)
		self.constraints = {'word_length':100, 'syllables_per_line': 10, 'tense':'present', 'person':'first'}
		self.key_phrases = None
		self.topic = None
		self.emotion = None
		self.poi = pool_of_ideas()

	def run(self):
		ex1 = analyzing_expert()
		ex1.run(self)

	def process_input(self, inspiration):
		'''
		lowers and tokenizes the input.
		'''
		inspiration = inspiration.lower()
		sents = [sent for sent in nltk.tokenize.sent_tokenize(inspiration)]
		words = [nltk.tokenize.word_tokenize(sent) for sent in sents]
		return words