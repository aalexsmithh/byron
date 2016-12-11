class template(object):
	"""docstring for template"""
	def __init__(self):
		super(template, self).__init__()
		self.pos = []
		self.token = []
		self.tfidf = []

	def add_raw(self,raw):
		for sent in raw:
			sent_raw = []
			sent_pos = []
			for word in sent:
				sent_raw.append(word[0])
				sent_pos.append(word[1])
			self.pos.append(sent_pos)
			self.token.append(sent_raw)

	def add_tfidf(tfidf_dict):
		for sent in self.token:
			tfidf_sent = []
			for word in sent:
				tfidf_sent.append(tfidf_dict[word])
			self.tfidf.append(tfidf_sent)
		