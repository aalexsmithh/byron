from byron.util.make_templates import *
from byron.util.util import *
import numpy as np

class sentence_expert(object):
	def __init__(self, token, pos, pos_flat, token_flat, template):
		super(sentence_expert, self).__init__()
		self.nodes = []
		self.sentences = []
		self.docs_token = token
		self.docs_pos = pos
		self.docs_pos_flat = pos_flat
		self.docs_token_flat = token_flat
		self.template = template
		self.p = None
		self.V = None
		
	def run(self):		
		

		# pos_tags = set([])
		# docs_token = load_from_file('token','hide/poems/encoded/', num_files=None)
		# docs_pos = load_from_file('pos','hide/poems/encoded/', num_files=None)
		# docs_pos_flat = flatten_text(docs_pos)
		# docs_token_flat = flatten_text(docs_token)

		# templates = make_template(self.docs_pos,None,20,2,True)

		print self.template
		#list of nodes with their pos tags
		self.subcorpus = self.get_subcorpus_for_template(self.docs_pos_flat,self.template,5)

		self.p = multithread_trigram_p(self.subcorpus,self.subcorpus,self.subcorpus,self.docs_pos_flat,with_pos=True)
		for word in self.p.keys()[0:10]:
			print word, self.heuristic_cost(word,1,1)

	def add_sentence(self,sent):
		self.sentences.append(sent)

	def search(self):
		'''
		runs IDA* search to find some candidate sentence
		'''


	def heuristic_cost(self,word,idx,max_len):
		# self.subcorpus indicates w1,w2 for each trigram
		if idx == max_len:
			return min([min(low) for low in self.p[word][:]]), max([max(low) for low in self.p[word][:]])

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

def make_sentence_experts(num_experts, token, pos, pos_flat, token_flat, template):
	# rng = random.SystemRandom()
	experts = []
	for i in range(num_experts):
		#make this random again
		experts.append(sentence_expert(token, pos, pos_flat, token_flat, template[np.random.randint(0, len(template))]))
		# experts.append(sentence_expert(token, pos, pos_flat, token_flat, template[rng.randint(0, len(template))]))
	return experts

def run_sentence_experts(experts):
	for i in range(len(experts)):
		experts[i].run()