from nltk import wordnet

class pool_of_ideas(object):
	def __init__(self):
		super(pool_of_ideas, self).__init__()
		self.nouns = []
		self.adjectives = []
		self.verbs = []
		self.comparisons = {}
		self.hypernyms = {}
		self.antonyms = {}
		self.synonyms = {}
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

	def add_synonym(self,list,single=False):
		'''
		assumes that a redundancy check has already been completed.
		input: (key,word)
		storage: {key, [word, ...]}
		'''
		if single:
			if self.synonyms.has_key(list[0]): #check if word exists
				if list[1] not in self.synonyms[list[0]]: #check if synonym already exists for word
					self.synonyms[list[0]].append(list[1]) #if not, add synonym
			else:
				self.synonyms[list[0]] = [list[1]]
		else:
			for a in list:
				if self.synonyms.has_key(a[0]): #check if word exists
					if a[1] not in self.synonyms[a[0]]: #check if synonym already exists for word
						self.synonyms[a[0]].append(a[1]) #if not, add synonym
				else:
					self.synonyms[a[0]] = [a[1]]

	def add_antonym(self,list,single=False):
		'''
		assumes that a redundancy check has already been completed.
		input: (key,word)
		storage: {key, [word, ...]}
		'''
		if single:
			if self.antonyms.has_key(list[0]): #check if word exists
				if list[1] not in self.antonyms[list[0]]: #check if synonym already exists for word
					self.antonyms[list[0]].append(list[1]) #if not, add synonym
			else:
				self.antonyms[list[0]] = [list[1]]
		else:
			for a in list:
				if self.antonyms.has_key(a[0]): #check if word exists
					if a[1] not in self.antonyms[a[0]]: #check if synonym already exists for word
						self.antonyms[a[0]].append(a[1]) #if not, add synonym
				else:
					self.antonyms[a[0]] = [a[1]]