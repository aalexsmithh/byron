import nltk
from byron.pool_of_ideas import pool_of_ideas
from byron.experts.analyzing_expert import analyzing_expert
from byron.experts.wordnet_expert import wordnet_expert
from byron.experts.keywords_expert import keywords_expert

class blackboard(object):
	def __init__(self,inspiration,constraints={}):
		super(blackboard, self).__init__()
		self.inspiration = self.process_input(inspiration)
		self.key_phrases = None
		self.topic = None
		self.emotion = None
		self.poi = pool_of_ideas()
		self.load_constraints(constraints)

	def run(self):
		ex1 = analyzing_expert()
		ex2 = wordnet_expert()
		ex3 = keywords_expert()
		# ex1.run(self)
		# ex2.run(self)
		ex3.run(self)

	def process_input(self, inspiration):
		'''
		lowers and tokenizes the input.
		'''
		inspiration = inspiration.lower()
		sents = [sent for sent in nltk.tokenize.sent_tokenize(inspiration)]
		words = [nltk.tokenize.word_tokenize(sent) for sent in sents]
		return words

	def load_constraints(self, constraints):
		'''
		word_length > 5
		syllables_per_line < word_length
		tense = [present, past]
		person = [first,second,third]

		defaults:
		'word_length':100, 'syllables_per_line': 10, 'tense':'present', 'person':'first'
		'''
		if constraints.has_key('word_length'):
			if constraints['word_length'] < 5:
				raise ValueError(constraints['word_length'], 'Word length must be greater than 5!')
			else:
				self.word_length = constraints['word_length']
		else:
			self.word_length = 100

		if constraints.has_key('syllables_per_line'):
			if constraints['syllables_per_line'] >= self.word_length:
				raise ValueError(constraints['syllables_per_line'], 'Syllables per line must be realistic for %i words!' % self.word_length)
			else:
				self.syllables_per_line = constraints['syllables_per_line']
		else:
			self.syllables_per_line = 5

		if constraints.has_key('tense'):
			if constraints['tense'] not in ['present','past']:
				raise ValueError(constraints['tense'], 'Must be present or past tense only')
			else:
				self.tense = constraints['tense']
		else:
			self.tense = 'present'
		
		if constraints.has_key('person'):
			if constraints['person'] not in ['first','second','third']:
				raise ValueError(constraints['person'], 'Must be in first, second, or third person only')
			else:
				self.person = constraints['person']
		else:
			self.person = 'first'