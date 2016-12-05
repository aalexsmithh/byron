from nltk import wordnet

class pool_of_ideas(object):
	"""docstring for pool_of_ideas"""
	def __init__(self):
		super(pool_of_ideas, self).__init__()
		self.nouns = []
		self.adjectives = []
		self.verbs = []
		self.comparisons = {}
		self.hypernyms = []
		self.antonyms = []
		self.emtotional_words = []
		self.phrases = []
		self.poem_draft = []
		
	def add_noun(self,list,single=False):
		if single:
			self.nouns.append(list)
		else:
			for a in list:
				self.nouns.append(a)

	def add_verb(self,list,single=False):
		if single:
			self.verbs.append(list)
		else:
			for a in list:
				self.verbs.append(a)

	def add_adjective(self,list,single=False):
		if single:
			self.adjectives.append(list)
		else:
			for a in list:
				self.adjectives.append(a)

	def add_comparison(self,list,single=False):
		'''
		input: (key,word)
		storage: {key, {word,count}}
		'''
		if single:
			if self.comparisons.has_key(list[0]): #if dict has adjective
				if self.comparisons[list[0]].has_key(list[1]): #if adjective has noun
					self.comparisons[list[0]][list[1]] += 1
				else: #if adjective doesn't have noun
					self.comparisons[list[0]][list[1]] = 1
			else: #if dict doensn't have adjective
				self.comparisons[list[0]] = {list[1]: 1}

		else:
			for a in list:
				if self.comparisons.has_key(a[0]): #if dict has adjective
					if self.comparisons[a[0]].has_key(a[1]): #if adjective has noun
						self.comparisons[a[0]][a[1]] += 1
					else: #if adjective doesn't have noun
						self.comparisons[a[0]][a[1]] = 1
				else: #if dict doensn't have adjective
					self.comparisons[a[0]] = {a[1]: 1}
