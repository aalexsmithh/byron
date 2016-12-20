import cPickle, sys, string
from byron.util.template import doc_template, sentence_template
from byron.util.decode import load_from_file


def _template_from_doc(doc,idf,tfidf):
	a = doc_template()
	a.add_raw(doc)
	a.add_tfidf(tfidf)
	a.add_idf(idf)
	a.make_template()
	return a

def make_template(docs, max_len=15, min_X=3, prune=True):
	'''
	docs must be the .pos files
	'''
	idf = cPickle.load(open('hide/idf.tfidf'))
	tfidf = cPickle.load(open('hide/byword.tfidf'))

	templates = []

	for key in docs.keys():
		templates.append(_template_from_doc(docs[key],idf[key],tfidf[key]))

	parsed_templates = []
	idx = 1
	f_num = len(templates)
	for t in templates:
		sys.stdout.write("\rAnalyzing templates from document %i of %i..." % (idx, f_num))
		sys.stdout.flush()
		idx += 1
		for i,sent in enumerate(t.template):
			if len(sent) < max_len:
				if sum(word == 'X' for word in sent) > min_X:
					parsed_templates.append(t.make_sent_template(i))
	print
	
	if prune:
		parsed_templates = prune_templates(parsed_templates)
	return parsed_templates

def prune_templates(templates):
	pruned = []

	punct_to_remove = [sym for sym in string.punctuation]
	for sym in ["!","?",".",",",";",":"]:
		punct_to_remove.remove(sym)

	idx = 1
	f_num = len(templates)
	remove = []
	for i in range(len(templates)):
		sys.stdout.write("\rPruning template %i of %i..." % (idx, f_num))
		sys.stdout.flush()
		idx += 1
		remove = False
		t = templates[i].template
		for punct in punct_to_remove:
			if t.count(punct) >= 1:
				remove = True
		if t[len(t)-1] == 'X':
			remove = True
		if not remove:
			pruned.append(templates[i])
	print

	print '\rRemoved %i templates in pruning operation...' % (len(templates) - len(pruned))
	return pruned


def main():
	tfidf = cPickle.load(open('../../hide/byword.tfidf'))
	docs = load_from_file('pos','../../hide/poems/encoded/')

	templates = []

	for key in docs.keys():
		templates.append(template_from_doc(docs[key],tfidf[key]))

	template[0]


if __name__ == '__main__':
	main()