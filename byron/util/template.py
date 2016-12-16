class doc_template(object):
	"""docstring for template"""
	def __init__(self):
		super(doc_template, self).__init__()
		self.pos = []
		self.token = []
		self.tfidf = []
		self.idf = []
		self.template = []

	def add_raw(self,raw):
		for sent in raw:
			sent_raw = []
			sent_pos = []
			for word in sent:
				sent_raw.append(word[0])
				sent_pos.append(word[1])
			self.pos.append(sent_pos)
			self.token.append(sent_raw)

	def add_tfidf(self,tfidf_dict):
		for sent in self.token:
			tfidf_sent = []
			for word in sent:
				try:
					tfidf_sent.append(tfidf_dict[word])
				except KeyError, e:
					tfidf_sent.append(float(0))
			self.tfidf.append(tfidf_sent)

	def add_idf(self,idf_dict):
		for sent in self.token:
			idf_sent = []
			for word in sent:
				try:
					idf_sent.append(idf_dict[word])
				except KeyError, e:
					idf_sent.append(float(0))
			self.idf.append(idf_sent)

	def make_template(self, threshold = 4):
		for i,sent in enumerate(self.token):
			sent_template = []
			for j,word in enumerate(sent):
				if self.idf[i][j] > threshold:
					sent_template.append('X')
				else:
					sent_template.append(word)
			self.template.append(sent_template)

	def make_sent_template(self,sent_idx):
		a = sentence_template()
		a.add_pos(self.pos[sent_idx])
		a.add_template(self.template[sent_idx])
		return a

class sentence_template(object):
	"""docstring for template"""
	def __init__(self):
		super(sentence_template, self).__init__()
		self.pos = []
		self.template = []
		self.force = []
		self.length = 0

	def __str__(self):
		str_ret = ''
		for i in xrange(self.length):
			str_ret += '[%s %s]' % (self.template[i],self.pos[i])
		return str_ret

	def add_pos(self,pos_sent):
		self.pos = pos_sent
		self.length = len(pos_sent)
		
	def add_template(self,template_sent):
		self.template = template_sent
		self.length = len(template_sent)

