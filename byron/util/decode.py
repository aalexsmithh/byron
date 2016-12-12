# from __future__ import print_function
from collections import Counter
import argparse, nltk, cPickle, sys, glob, random, math, operator, string
from matplotlib import pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

random.seed(1337)

def encode_poems():
	parser = argparse.ArgumentParser()
	parser.add_argument("files", nargs='+')
	args = parser.parse_args()


	for path in args.files:#[0:2]:
		# print path
		f = open(path,'rb')
		text = [s.decode('iso-8859-1').encode('ascii','ignore') for s in f.readlines()]
		f.close()

		# start = [(i,s) for i,s in enumerate(text) if 'START OF' in s]
		# end = [(i,s) for i,s in enumerate(text) if 'End of' in s]
		# if start == []:
		# 	print 'a', path
		# if end == []:
		# 	end = [(i,s) for i,s in enumerate(text) if 'END OF' in s]
		# 	if end == []:
		# 		print 'b', path

		pth = path[:32] + path[38:-4] + '.poem' 
		f = open(pth, 'wb')
		# frm = start[0][0]
		# to = end[0][0]
		# # print frm, to
		# text_wo_intro_outro = text[frm+1:to]
		f.write(''.join(text))
		f.close()

def pos_tag_poems():
	parser = argparse.ArgumentParser()
	parser.add_argument("files", nargs='+')
	args = parser.parse_args()

	# pos_tag = nltk.tag.perceptron.PerceptronTagger()
	idx = 1
	files = len(args.files)
	for path in args.files:
		sys.stdout.write("\rDocument %i of %i processed" % (idx, files))
		sys.stdout.flush()
		# print 'Document %i of %i processed\r' % (idx, files)
		f = open(path,'rb')
		text = f.read()
		f.close()

		text = process_input(text)

		# text_tags = []
		# for sent in text:
		# 	tags = pos_tag.tag(sent)
		# 	text_tags.append(tags)

		pth = path[:25] + path[25:-5] + '.token' 
		with open(pth, 'wb') as fp:
			cPickle.dump(text, fp)
		idx += 1
	print

# @profile
def load_from_file(filetype,path,num_files=None):
	'''
	filetype of the files wising to be opened.
	path leads to the folder that contains the files wishing to be opened.
	'''
	pth = path + '*.' + filetype
	files = glob.glob(pth)

	data = {}

	if num_files is None:
		num_files = len(files)
	i = 1
	f_num = num_files
	random.shuffle(files)
	for f in files[:num_files]:
		sys.stdout.write("\rLoading %i of %i..." % (i, f_num))
		sys.stdout.flush()
		idx = f[len(path):-len(filetype)-1]
		if filetype == 'poem':
			data[idx] = open(f,'rb').read()
		else:
			data[idx] = cPickle.load(open(f,'rb'))
		i += 1
	print
	return data

def pos_templates(docs):
	pos_template = []
	for doc in docs.values():
		for sent in doc:
			for word in sent:
				pass

# @profile
def tf_idf(docs):
	'''
	docs must be the tokenized documents loaded from load_from_file()
	'''
	punct = string.punctuation
	a = docs.values()
	words = sorted(set([word for doc in a for sent in doc for word in sent]))
	dictionary = {}
	dictionary_reversed = {}
	i = 0
	for word in words:
		dictionary[word] = i
		dictionary_reversed[i] = word
		i += 1
	
	keys = docs.keys()
	# idx = 1
	# f_num = len(keys)
	# for key in keys:
	# 	sys.stdout.write("\rEncoding document %i of %i..." % (idx, f_num))
	# 	sys.stdout.flush()
	# 	idx += 1
	# 	docs[key] = [[dictionary[word] for word in sent] for sent in docs[key]]
	# 	# this = [one_hot(dictionary[word],word_count) for sent in this for word in sent]
	# print

	tf_doc = {}
	idf = {}
	idx = 1
	f_num = len(keys)
	for key in keys:
		sys.stdout.write("\rtf-idf of document %i of %i..." % (idx, f_num))
		sys.stdout.flush()
		idx += 1
		word_count = 0
		this = docs[key]
		tf = {}
		uniques = set([])
		
		for sent in this:
			for word in sent:
				
				if word not in uniques:
					uniques.add(word)
					if idf.has_key(word):
						idf[word] += 1
					else:
						idf[word] = 1

				word_count += 1
				if tf.has_key(word):
					tf[word] += 1
				else:
					tf[word] = 1
		
		for t in tf.keys():
			tf[t] = float(tf[t]+1)/float(word_count+len(uniques))
		tf_doc[key] = tf
	print

	for df in idf.keys():
		idf[df] = float(len(keys))/float(idf[df])

	tfidf = {}
	for key in keys:
		for t in tf_doc[key].keys():
			# tf_doc[key][t] = tf_doc[key][t]/float(math.log(idf[t]))
			tf_doc[key][t] = idf[t]

		tfidf[key] = tf_doc[key]

	return tfidf

def one_hot(idx,count):
	oh = np.zeros(count,dtype='int_')
	oh[idx] = 1
	return oh.tolist()

def sent_stats(docs):
	sent_lens = []
	pos_tags = []
	for doc in docs.values():
		for sent in doc:
			sent_lens.append(len(sent))
			for word in sent:
				pos_tags.append(word[1])

	plt.barh(Counter(sent_lens).keys(), Counter(sent_lens).values(), align='center', alpha=0.5)
	plt.show()

	# for pos in zip()
	print 'sentence analysis:'
	print Counter(sent_lens).keys()
	print
 	print Counter(sent_lens).values()

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

def process_input(text):
		'''
		lowers and tokenizes the input.
		'''
		text = text.lower()
		sents = [sent for sent in nltk.tokenize.sent_tokenize(text)]
		words = [nltk.tokenize.word_tokenize(sent) for sent in sents]
		return words

if __name__ == '__main__':
	d = load_from_file('token','../../hide/poems/encoded/')
	a = tf_idf(d)
	f = open('idf.tfidf','wb')
	cPickle.dump(a,f)
	f.close()

	# sent_stats(d)