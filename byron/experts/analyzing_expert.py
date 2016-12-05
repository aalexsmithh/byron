import nltk, string

class analyzing_expert(object):
	"""docstring for analyzing_expert"""
	def __init__(self):
		super(analyzing_expert, self).__init__()
		
	def run(self,bb):
		'''
		initiates the analyzing expert for one round of analysis. 
		bb is the working blackboard that is analyzed.

		notes:
		1. lemma, rm_stops
		2. pos tag
		3. add each to the poi on the bb
		'''

		text = bb.inspiration
		text_tags = []

		pos_tag = nltk.tag.perceptron.PerceptronTagger()

		for sent in text:
			tags = pos_tag.tag(sent)
			text_tags.append(tags)

		#get nouns, verbs, and adjectives
		for sent in text_tags:
			for word in sent:
				if word[0] not in nltk.corpus.stopwords.words('english') and word[0] not in string.punctuation:
					if word[1][0:2] == 'NN' and word[0] not in bb.poi.nouns:
						bb.poi.add_noun(word[0],True)
					if word[1][0:2] == 'VB' and word[0] not in bb.poi.verbs:
						bb.poi.add_verb(word[0],True)
					if word[1][0:2] == 'JJ' and word[0] not in bb.poi.adjectives:
						bb.poi.add_adjective(word[0],True)
		
		#get comparisons
		for sent in text_tags:
			for i in range(len(sent)):
				if sent[i][1][0:2] == "JJ" and sent[i+1][1][0:2] == 'NN':
					bb.poi.add_comparison((sent[i][0],sent[i+1][0]),True)

		print bb.poi.comparisons


