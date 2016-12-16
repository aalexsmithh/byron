from byron.util.make_templates import *
from byron.util.util import *

class sentence_expert(object):
	def __init__(self, token, pos, pos_flat, token_flat, template):
		super(sentence_expert, self).__init__()
		self.nodes = []
		self.sentences = []
		self.docs_token = token
		self.docs_pos = pos
		self.docs_pos_flat = pos_flat
		self.docs_token_flat = token_flat
		self.templates = template
		
	def run(self):		
		rng = random.SystemRandom()

		# pos_tags = set([])
		# docs_token = load_from_file('token','hide/poems/encoded/', num_files=None)
		# docs_pos = load_from_file('pos','hide/poems/encoded/', num_files=None)
		# docs_pos_flat = flatten_text(docs_pos)
		# docs_token_flat = flatten_text(docs_token)

		# templates = make_template(self.docs_pos,None,20,2,True)
		sent_temp = self.templates[rng.randint(0, len(templates))]
		print sent_temp

		#list of nodes with their pos tags
		subcorpus = self.get_subcorpus_for_template(self.docs_pos_flat,sent_temp)

		# print subcorpus

		# print word_pos['VBZ']

		multithread_trigram_p(subcorpus,subcorpus,subcorpus,self.docs_pos_flat,with_pos=True)

	def add_sentence(self,sent):
		self.sentences.append(sent)

	def search(self):
		'''
		runs IDA* search to find some candidate sentence
		'''

	def get_subcorpus_for_template(self, docs, template, corp_mult=30):
		'''
		corp_mult is the multiple of words that should be grabbed. it is multiplied by the number of open slots in the template
		'''
		pos_tags = {}
		for i,pos in enumerate(template.pos):
			if template.template[i] != 'X':
				pass
			else:
				if pos_tags.has_key(pos):
					pos_tags[pos] += 1
				else:
					pos_tags[pos] = 1

		tags = []
		counts = []
		for pos in pos_tags.keys():
			if pos not in tags:
				tags.append(pos)
				counts.append(pos_tags[pos]*corp_mult)

		#convert to accept flat_text
		# docs = flatten_text(docs)

		words = get_words_with_tags(docs,counts,tags,True)

		return words