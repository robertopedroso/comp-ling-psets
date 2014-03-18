digraphs = {'ai': 'ai', 'ei': 'ei', 'oi': 'ɔi', 'ui': 'i', 'au': 'aʊ',
	'eu': 'eu', 'ou': 'o', 'dd': 'ɟ', 'll': 'ʎ', 'rr': 'r', 'ts': 'ts̺',
	'tt': 'c', 'tx': 'tʃ', 'tz': 'ts̻', 'ch': 'tʃ'}
idigraphs = {'in': 'iɲ', 'it': 'ic', 'id': 'iɟ', 'il': 'iʎ'}
monographs = {'ñ': 'ɲ', 's': 's̺', 'q': 'k', 'x': 'ʃ', 'y': 'j', 'z': 's̻',}

# matches a grapheme against a dict of grapheme-phoneme mappings
def match_rule(grapheme, mappings):
	if grapheme in mappings:
		return mappings[grapheme]
	
	return False

# calls match_rule() for a digraph only if current grapheme is not at end of word
def digraph_check(i, graphemes):
	if i+1 < len(graphemes):
		digraph = graphemes[i] + graphemes[i+1]
		return match_rule(digraph, digraphs)
		
	return False

# j followed by e is /x/ otherwise /j/
def j_rule(i, graphemes):
	if i+1 < len(graphemes) and graphemes[i+1] == 'e':
		return 'x'
		
	return 'j'

# non-terminal b is /β/, otherwise /b/
def b_rule(i, graphemes):
	if i == 0 or i+1 == len(graphemes):
		return 'b'

	return 'β'

# r- and -r are trills but -r- is a tap
# -rr- is also a trill but will be caught by digraph_check()
def r_rule(i, graphemes):
	if i == 0 or i+1 == len(graphemes):
		return 'r'

	return 'ɾ'

# i is /i/ except when -in-, -it-, -id-, -il-
def i_rule(i, graphemes):
	if i != 0 and i+2 <= len(graphemes) and graphemes[i+1] in ['n', 't', 'd', 'l']:
		digraph = graphemes[i] + graphemes[i+1]
		return match_rule(digraph, idigraphs)

	return False

def c_rule(i, graphemes):
	if i+1 < len(graphemes) and graphemes[i+1] in ['e', 'i']:
		return 's'

	return 'k'

# returns a single char representing the position of a grapheme in a word
def transcribe(word):
	graphemes = list(word)
	transcription = list()

	i = 0
	while i < len(graphemes):
		digraph_match = digraph_check(i, graphemes)
		if digraph_match is not False:
			transcription.append(digraph_match)
			i += 2
			continue

		if graphemes[i] == 'j':
			transcription.append(j_rule(i, graphemes))
			i += 1
			continue

		if graphemes[i] == 'b':
			transcription.append(b_rule(i, graphemes))
			i += 1
			continue

		if graphemes[i] == 'r':
			transcription.append(r_rule(i, graphemes))
			i += 1
			continue

		if graphemes[i] == 'i':
			idigraph_match = i_rule(i, graphemes)
			if idigraph_match is not False:
				transcription.append(idigraph_match)
				i += 2
			else:
				transcription.append('i')
				i += 1

			continue

		if graphemes[i] == 'c' or graphemes[i] == 'ç':
			transcription.append(c_rule(i, graphemes))
			i += 1
			continue

		# no more special rules; attempt to match monographs
		# if we don't find a match then the letter and its IPA are the same
		monograph_check = match_rule(graphemes[i], monographs)
		if monograph_check is not False:
			transcription.append(monograph_check)
		else:
			transcription.append(graphemes[i])	

		i += 1
		continue
	
	# we need our phonetic transcription to be whitespace-delimited IPA
	return ' '.join(transcription)

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='Generates a phonetic representation of a Basque word.')

	parser.add_argument('word', type=str, help='the word to be transcribed')
	args = parser.parse_args()

	print(transcribe(args.word))
