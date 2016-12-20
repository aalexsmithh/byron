from byron.util.make_templates import *
from byron.util.util import *
import numpy as np
import sys, time, math

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
		self.trigram = None
		self.bigram = None
		self.unigram = None
		self.V = None
		
	def run(self):		
		delta = 1e-10

		# pos_tags = set([])
		# docs_token = load_from_file('token','hide/poems/encoded/', num_files=None)
		# docs_pos = load_from_file('pos','hide/poems/encoded/', num_files=None)
		# docs_pos_flat = flatten_text(docs_pos)
		# docs_token_flat = flatten_text(docs_token)

		# templates = make_template(self.docs_pos,None,20,2,True)

		print self.template
		
		template_mult = 50
		self.subcorpus = self.get_subcorpus_for_template(self.docs_pos_flat,self.template,template_mult)
		#early cutoff just in case
		if len(self.subcorpus) > template_mult*len(self.template.template):
			# print 'too many values'
			return 0
		if len(self.subcorpus) < (template_mult/4)*len(self.template.template):
			# print 'not enough values'
			return 0

		# self.calc_all_bigrams(self.docs_pos_flat)

		# trigram_p_pos(self.subcorpus,self.subcorpus,self.subcorpus[0],self.docs_pos_flat,delta=1e-13)

		# print self.subcorpus

		# for i in range(50):
		# 	w = self.docs_pos_flat[np.random.randint(0,len(self.docs_pos_flat))]
		# 	print i, w
		# 	print bigram_p_pos(self.docs_pos_flat,w,self.docs_pos_flat,1e-8)

		self.trigram = multithread_trigram_p(self.subcorpus,self.subcorpus,self.subcorpus,self.docs_pos_flat,delta,with_pos=True)
		self.bigram = bigram_p_pos(self.subcorpus,self.subcorpus,self.docs_pos_flat, delta)
		self.unigram = unigram_p_pos(self.subcorpus, self.docs_pos_flat, delta)

		
		self.search()

		# for i, slot in enumerate(self.template):
		# 	if slot[0] != 'X':
		# 		print slot[0]
		# 	if slot[0] == 'X':
		# 		for word in self.trigram.keys():
		# 			if word[1] == slot[1] and i == 0:
		# 				print self.unigram
		# 			if word[1] == slot[1] and i == 1:
		# 				pass
		# 			if word[1] == slot[1] and i >= 2:
		# 				print '\t',self.heuristic_cost(word,1,1,self.template.pos[i-2],self.template.pos[i-1]), word
		# 		print 

	def add_sentence(self,sent):
		self.sentences.append(sent)

	def search(self):
		'''
		runs IDA* search to find some candidate sentence
		'''
		sentence = []
		for i, slot in enumerate(self.template):
			if slot[0] != 'X':
				print slot[0],
				sentence.append(slot)
			if slot[0] == 'X':
				if i == 0:
					a = self.get_max_unigram(slot[1])[1]
					print a[0],
					sentence.append(a)

				if i == 1:
					a = self._search_bi(sentence[i-1],self.bigram.keys(),slot[1])[1]
					print a[0],
					sentence.append(a)

				if i >= 2:
					a = self._search_tri(sentence[i-2],sentence[i-1],self.trigram.keys(),slot[1])[1]
					print a[0],
					sentence.append(a)
		print

	def _search_tri(self,w1,w2,w3,w3_pos):
		#find best of w3 for fixed w1 and w2
		best = []
		for w in w3:
			if w[1] == w3_pos:
				best.append( (self.trigram[w][self.subcorpus.index(w1),self.subcorpus.index(w2)],w,self.subcorpus.index(w1),self.subcorpus.index(w2)) )
		a = max(best,key = lambda t: t[0])
		self.trigram[a[1]] = self.trigram[a[1]] ** 2 #[a[2],a[3]] = (self.trigram[a[1]][a[2],a[3]] * self.trigram[a[1]][a[2],a[3]])
		# print 'best trigram is', a, 'new p is now', self.trigram[a[1]][a[2],a[3]]
		return a[0:2]

	def _search_bi(self,w1,w2,w2_pos):
		best = []
		for w in w2:
			if w[1] == w2_pos:
				best.append( (self.bigram[w][self.subcorpus.index(w1)],w,self.subcorpus.index(w1)) )
		a = max(best,key = lambda t: t[0])
		self.bigram[a[1]] = self.bigram[a[1]] ** 2# = (self.bigram[a[1]][a[2]] * self.bigram[a[1]][a[2]])
		# print 'best bigram is', a, 'new p is now', self.bigram[a[1]][a[2]]
		return a[0:2]

	def calc_all_bigrams(self,corpus): 
		corpus = list(set(corpus))
		bigrams = {}
		for word in corpus:
			bigrams[word] = bigram_p_pos(self.docs_pos_flat,word,self.docs_pos_flat)
		print
		print sys.getsizeof(bigrams)/1024/1024, 'mb'

	def heuristic_cost(self,word,idx,max_len,pos_1,pos_2): #constrain this so it only looks at p's with the correct pos tags
		# self.subcorpus indicates w1,w2 for each trigram
		if idx == max_len:
			total = []
			for i,row in enumerate(self.trigram[word][:]):
				rows = []
				for j, val in enumerate(row[:]):
					# print self.subcorpus[i], self.subcorpus[j]
					if self.subcorpus[i][1] == pos_1 and self.subcorpus[j][1] == pos_2: #switched the i and j
						rows.append(( math.log(val), self.subcorpus[i], self.subcorpus[random.sample(np.where(row==val)[0],1)[0]] ))
				# rows.append(min([(math.log(val),i,np.where(row==val)) for val in row],key = lambda t: t[0]))
				if len(rows) != 0:
					total.append(min(rows,key = lambda t: t[0]))
			return min(total,key = lambda t: t[0])
			# return min([min([math.log(val) for val in row]) for row in self.trigram[word][:]])
			# return min([min(math.log(low)) for low in self.trigram[word][:] for sent in ])#, max([max(low) for low in self.trigram[word][:]])

	def get_max_unigram(self,pos):
		return max([(self.unigram[i],word) for i,word in enumerate(self.subcorpus) if word[1] == pos],key = lambda t: t[0])


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
		# print counts
		# print tags
		words = get_words_with_tags(docs,counts,tags,True)

		#add the forced tags from the main set
		for word in template:
			if word[0] != 'X':
				words.append(word)

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