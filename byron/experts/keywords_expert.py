import nltk, string

class keywords_expert(object):
	def __init__(self):
		super(keywords_expert, self).__init__()
		
	def run(self,bb):
		'''
		initiates the analyzing expert for one round of analysis. 
		bb is the working blackboard that is analyzed.
		'''
		# parser = nltk.ChartParser(groucho_grammar)
		# for tree in parser.parse(sent):
		# 	print(bb.inspiration)

		text = bb.inspiration
		text_tags = []

		pos_tag = nltk.tag.perceptron.PerceptronTagger()

		for sent in text:
			tags = pos_tag.tag(sent)
			text_tags.append(tags)

		grammar = "NP: {<DT>?<JJ>*<NN>}"
		cp = nltk.RegexpParser(grammar)
		NPs = []
		for sent in text_tags:
			result = cp.parse(sent)
			for p in result:
				try:
					assert not isinstance(p[0], basestring)
					np_toadd = []
					for a in p:
						np_toadd.append(a[0])
					if ' '.join(np_toadd) not in NPs:
						NPs.append(' '.join(np_toadd))
				except Exception, e:
					pass
		
		bb.key_phrases = NPs

		# for kp in bb.key_phrases: #find which has highest inspiration score
			

		print bb.key_phrases