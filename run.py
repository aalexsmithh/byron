from byron.blackboard import blackboard
from nltk.corpus import treebank
from nltk import treetransforms
from nltk import induce_pcfg
from nltk.parse import pchart
from nltk import nonterminals, Production#, parse_pcfg
from nltk import PCFG

def main():
	insp = "When he was nearly thirteen, my brother Jem got his arm badly broken at the elbow. \
			When it healed, and Jem's fears of never being able to play football were assuaged, \
			he was seldom self-conscious about his injury. His left arm was somewhat shorter \
			than his right; when he stood or walked, the back of his hand was at right angles to \
			his body, his thumb parallel to his thigh. He couldn't have cared less, so long as he \
			could pass and punt. When enough years had gone by to enable us to look back on them, \
			we sometimes discussed the events leading to his accident. I maintain that the Ewells \
			started it all, but Jem, who was four years my senior, said it started long before that. \
			He said it began the summer Dill came to us, when Dill first gave us the idea of \
			making Boo Radley come out. There were enough years and enough crap for your mother."

	insp2 = "Testing the large System. this is Downright Crazy, Insane, and absurd!"
	a = blackboard(insp)
	a.run()

def test():

	toy_pcfg1 = parse_pcfg("""
		S -> NP VP [1.0]
		NP -> Det N [0.5] | NP PP [0.25] | 'John' [0.1] | 'I' [0.15]
		Det -> 'the' [0.8] | 'my' [0.2]
		N -> 'man' [0.5] | 'telescope' [0.5]
		VP -> VP PP [0.1] | V NP [0.7] | V [0.2]
		V -> 'ate' [0.35] | 'saw' [0.65]
		PP -> P NP [1.0]
		P -> 'with' [0.61] | 'under' [0.39]
		""")

	pcfg_prods = toy_pcfg1.productions()

	pcfg_prod = pcfg_prods[2]
	print 'A PCFG production:', `pcfg_prod`
	print '    pcfg_prod.lhs()  =>', `pcfg_prod.lhs()`
	print '    pcfg_prod.rhs()  =>', `pcfg_prod.rhs()`
	print '    pcfg_prod.prob() =>', `pcfg_prod.prob()`
	print

	# extract productions from three trees and induce the PCFG
	print "Induce PCFG grammar from treebank data:"

	productions = []
	for item in treebank.items[:2]:
		for tree in treebank.parsed_sents(item):
			# perform optional tree transformations, e.g.:
			tree.collapse_unary(collapsePOS = False)    # Remove branches A-B-C into A-B+C
			tree.chomsky_normal_form(horzMarkov = 2)    # Remove A->(B,C,D) into A->B,C+D->D

			productions += tree.productions()

	S = Nonterminal('S')
	grammar = induce_pcfg(S, productions)
	print grammar
	print

if __name__ == '__main__':
	main()