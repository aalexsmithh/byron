import nltk, string
from nltk.corpus import wordnet as wn 

class wordnet_expert(object):
	def __init__(self):
		super(wordnet_expert, self).__init__()
		
	def run(self,bb):
		'''
		initiates the analyzing expert for one round of analysis. 
		bb is the working blackboard that is analyzed.
		'''
		self.find_antonyms(bb,bb.poi.adjectives)
		self.find_antonyms(bb,bb.poi.nouns)
		self.find_antonyms(bb,bb.poi.verbs)
		self.find_synonyms(bb,bb.poi.adjectives)
		self.find_synonyms(bb,bb.poi.nouns)
		self.find_synonyms(bb,bb.poi.verbs)

	def find_synonyms(self,bb,words,max_lookups=2):
		'''
		finds synonyms for words, and adds them to the poi using the add_synonym() method.
		only looks at the max_lookups most common synonyms.
		'''
		for word in words:
			synonyms = []
			for synset in wn.synsets(word):
				for lemma in synset.lemmas():
					synonyms.append((lemma.count(),lemma.name()))
			for i in range(max_lookups):
				if len(synonyms) != 0:
					syn = max(synonyms)
					if syn[1] != word:
						bb.poi.add_synonym((word,syn[1]),True)
					synonyms.remove(syn)
			

	def find_hypernyms(self,bb,words):
		'''
		unsure if wanting to complete.
		'''
		pass

	def find_antonyms(self,bb,words,max_lookups=2):
		'''
		finds antonyms for words, and adds them to the poi using the add_antonym() method.
		only looks at the max_lookups most common antonyms.
		'''
		for word in words:
			antonyms = []
			for synset in wn.synsets(word):
				for lemma in synset.lemmas():
					for ant in lemma.antonyms():
						antonyms.append((ant.count(),ant.name()))
			for i in range(max_lookups):
				if len(antonyms) != 0:
					ant = max(antonyms)
					bb.poi.add_antonym((word,ant[1]),True)
					antonyms.remove(ant)

		# j.antonyms()