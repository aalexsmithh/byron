import numpy as np
from multiprocessing.pool import ThreadPool
import multiprocessing, Queue

def word_count(docs_dict):
	count = 0
	words = set([])
	for key in docs_dict.keys():
		for sent in docs_dict[key]:
			for word in sent:
				words.add(word)
				count += 1
	print count, 'words, of which', len(words), 'are unique'
	return count, len(words)

#deprecated
def trigram(flat_text,w1,w2,w3,verbose=0):
	'''
	requires a np array for flat_text.
	w3 is the target word in this search p(w3|w1,w2)
	'''
	# print 'finding trigrams for %s | %s, %s' % (w3,w1,w2)
	# w1 = np.where(flat_text == w1)[0]
	# w2 = np.where(flat_text == w2)[0]
	# w3 = np.where(flat_text == w3)[0]
	# w1w2_ = []
	# w1_w3 = []
	# w1w2w3 = []
	count = 0
	# for idx in w1:
	# 	w1w2_ = np.where(w2 == idx+1)[0]
	# 	w1_w3 = np.where(w3 == idx+2)[0]
	# 	for idx2 in w1w2_:
	# 		w1w2w3 = np.where(w3 == w2[idx2]+1)[0]
	# 		if w1w2w3.shape[0] > 0:
	# 			# print w1w2w3
	# 			for idx in w1w2w3:
	# 				count += 1
	# 				if verbose == 1:
	# 					print flat_text[w3[idx]-4:w3[idx]+2]
	# if verbose == 1:
	# 	print

	for i,word in enumerate(flat_text):
		if word == w3:
			if flat_text[i-1] == w2:
				if flat_text[i-2] == w1:
					count += 1
	return count

#deprecated
def bigram(flat_text,w1,w2,verbose=0):
	'''
	requires a np array for the flat_text
	w2 is the target word in this search p(w2|w1)
	'''
	# print 'finding bigrams for %s | %s' % (w2,w1)
	# w1 = np.where(flat_text == w1)[0]
	# w2 = np.where(flat_text == w2)[0]
	# w1w2 = []
	count = 0
	# for idx in w1:
	# 	w1w2 = np.where(w2 == idx+1)[0]
	# 	if w1w2.shape[0] > 0:
	# 		for idx in w1w2:
	# 			count += 1
	# 			if verbose == 1:
	# 				print flat_text[w2[idx]-3:w2[idx]+2]
	# if verbose == 1:
	# 	print

	for i,word in enumerate(flat_text):
		if word == w2:
			if flat_text[i-1] == w1:
				count += 1
	return count

def multithread_trigram_p(w1,w2,w3,flat_text,delta=1e-8):
	# pool = ThreadPool(processes=5)
	processes = []

	idx = [0, int(0.20*len(w3)), int(0.40*len(w3)), int(0.60*len(w3)), int(0.80*len(w3)),len(w3)]
	#processes
	manager = multiprocessing.Manager()
	return_dict = manager.dict()
	t1 = multiprocessing.Process(target=_thread_trigram_p,args=(w1,w2,w3[idx[0]:idx[1]],flat_text,delta,return_dict,"t1"))
	processes.append(t1)
	t1.start()
	t2 = multiprocessing.Process(target=_thread_trigram_p,args=(w1,w2,w3[idx[1]:idx[2]],flat_text,delta,return_dict,"t2"))
	processes.append(t2)
	t2.start()
	t3 = multiprocessing.Process(target=_thread_trigram_p,args=(w1,w2,w3[idx[2]:idx[3]],flat_text,delta,return_dict,"t3"))
	processes.append(t3)
	t3.start()
	t4 = multiprocessing.Process(target=_thread_trigram_p,args=(w1,w2,w3[idx[3]:idx[4]],flat_text,delta,return_dict,"t4"))
	processes.append(t4)
	t4.start()
	t5 = multiprocessing.Process(target=_thread_trigram_p,args=(w1,w2,w3[idx[4]:idx[5]],flat_text,delta,return_dict,"t5"))
	processes.append(t5)
	t5.start()

	#threads
	# t1 = pool.apply_async(_thread_trigram_p, (w1,w2,w3[idx[0]:idx[1]],flat_text,delta,t1_ret))
	# t2 = pool.apply_async(_thread_trigram_p, (w1,w2,w3[idx[1]:idx[2]],flat_text,delta,t2_ret))
	# t3 = pool.apply_async(_thread_trigram_p, (w1,w2,w3[idx[2]:idx[3]],flat_text,delta,t3_ret))
	# t4 = pool.apply_async(_thread_trigram_p, (w1,w2,w3[idx[3]:idx[4]],flat_text,delta,t4_ret))
	# t5 = pool.apply_async(_thread_trigram_p, (w1,w2,w3[idx[4]:idx[5]],flat_text,delta,t5_ret))
	# t1_ret = t1.get()
	# t2_ret = t2.get()
	# t3_ret = t3.get()
	# t4_ret = t4.get()
	# t5_ret = t5.get()

	for p in processes:
		p.join()

	for key in return_dict.keys():
		print return_dict[key]

	print 'done'

	# print t1_ret, t2_ret, t3_ret, t4_ret, t5_ret


def _thread_trigram_p(w1,w2,w3,flat_text,delta,out_q,pid):
	print "starting thread"
	p = []
	for w in w3:
		p.append(trigram_p(w1,w2,w,flat_text,delta))
		print 'got trigram'
	# out_q.put(p)
	out_q[pid] = p


# @profile
def trigram_p(w1,w2,w3,flat_text, delta=None):
	'''
	w3 is a single word, w1 & w2 are lists of words to find trigrams for
	'''
	tri_counts = np.zeros((len(w1),len(w2)))
	bi_counts = np.zeros((len(w1),len(w2)))
	w1_set = set(w1)
	w2_set = set(w2)
	stop = len(flat_text)-2

	for i in xrange(flat_text.shape[0]):
		# if flat_text[i] == w3:
		# 	if flat_text[i-2] in w1_set:
		# 		if flat_text[i-1] in w2_set:
		# 			counts[w1.index(flat_text[i-2]),w2.index(flat_text[i-1])] += 1
		if flat_text[i] in w1_set:
			if i >= stop:
				break
			if flat_text[i+1] in w2_set:
				if flat_text[i+2] == w3:
					tri_counts[w1.index(flat_text[i]),w2.index(flat_text[i+1])] += 1
				bi_counts[w1.index(flat_text[i]),w2.index(flat_text[i+1])] += 1

	p = np.zeros((len(w1),len(w2)))
	bigram_smooth = float(delta)*float(len(flat_text) + len(flat_text)**2)
	for i in xrange(len(w1)):
		for j in xrange(len(w2)):
			p[i,j] = (float(tri_counts[i,j]) + float(delta)) / (float(bi_counts[i,j]) + bigram_smooth)

	# c_123 = trigram(flat_text,w1,w2,w3)
	# c_12 = bigram(flat_text,w1,w2)
	# if delta is not None:
	# 	c_123 = float(c_123) + delta
	# 	c_12 = float(c_12) + float(delta)*float(len(flat_text) + len(flat_text)**2)
	# return float(c_123)/float(c_12)

	return p

def random_word(docs,num_words=50):
	'''
	either takes a dict loaded from load_from_file() or a flattened numpy array
	'''
	if type(docs) is dict:
		text = flatten_text(docs)
	else:
		text = docs
	np.random.seed(1337)
	words = set([])
	length = len(text)
	while len(words) < num_words:
		words.add(text[np.random.randint(0,length)])
	return list(words)

def flatten_text(text):
	'''
	only takes a dict loaded by load_from_file in decode.py
	'''
	flat = [word for key in text.keys() for sent in text[key] for word in sent]
	flat = np.asarray(flat, dtype="string_")
	return flat
