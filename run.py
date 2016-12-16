from byron.blackboard import blackboard
import random
from byron.experts.sentence_expert import *
from byron.util.util import *

def main():
	# insp = "When he was nearly thirteen, my brother Jem got his arm badly broken at the elbow. \
	# 		When it healed, and Jem's fears of never being able to play football were assuaged, \
	# 		he was seldom self-conscious about his injury. His left arm was somewhat shorter \
	# 		than his right; when he stood or walked, the back of his hand was at right angles to \
	# 		his body, his thumb parallel to his thigh. He couldn't have cared less, so long as he \
	# 		could pass and punt. When enough years had gone by to enable us to look back on them, \
	# 		we sometimes discussed the events leading to his accident. I maintain that the Ewells \
	# 		started it all, but Jem, who was four years my senior, said it started long before that. \
	# 		He said it began the summer Dill came to us, when Dill first gave us the idea of \
	# 		making Boo Radley come out. There were enough years and enough crap for your mother."

	# insp2 = "Testing the large System. this is Downright Crazy, Insane, and absurd!"
	# a = blackboard(insp)
	# a.run()

	docs_token = load_from_file('token','hide/poems/encoded/', num_files=None)
	docs_pos = load_from_file('pos','hide/poems/encoded/', num_files=None)
	docs_pos_flat = flatten_text(docs_pos)
	docs_token_flat = flatten_text(docs_token)
	templates = make_template(docs_pos,None,20,2,True)

	a = sentence_expert(docs_token, docs_pos, docs_pos_flat, docs_token_flat, templates)
	a.run()

if __name__ == '__main__':
	main()