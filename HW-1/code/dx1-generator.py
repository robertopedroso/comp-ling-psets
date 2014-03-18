import csv, glob
import regex
from collections import Counter
from basque_pronunciation import transcribe

# tokenizes corpus document into a list of words
def tokenize_corpus(corpus):
	return regex.findall('\p{alpha}+', open(corpus, 'r').read().lower())

# parses a corpus document or directory and returns a uniqified list of words
def parse_corpus(corpus, recursive, n):
	words = list()

	if recursive is True:
		for file in glob.glob(corpus + '/*'):
			words.extend(tokenize_corpus(file))
	else:
		words = tokenize_corpus(file)

    # given a list of words returns a list of n word, frequency tuples
	return Counter(words).most_common(n)

# given a corpus corpus retuns 
def make_dictionary(words, outfile, delimiter):
    dictionary = [(w, f, transcribe(w)) for w,f in words]

    writer = csv.writer(outfile, delimiter=delimiter)
    for word, freq, phonemes in dictionary:
      writer.writerow([word, freq, phonemes])

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='Extracts unique words and word frequency from corpus documents.')

	parser.add_argument('-r', '--recursive', action='store_true', help='pull corpus documents recursively from a directory')
	parser.add_argument('-n', '--number', action='store', default=1000, type=int, help='maximum number of words to return; defaults to 1000')
	parser.add_argument('-d', '--delimiter', action='store', default='\t', help='delimiter to use in dx1 file output')
	parser.add_argument('corpus', type=str, help='path corpus document or directory')
	parser.add_argument('outfile', type=argparse.FileType('w'), help='name of output file')
	args = parser.parse_args()

	words = parse_corpus(args.corpus, args.recursive, args.number)
	make_dictionary(words, args.outfile, args.delimiter)
