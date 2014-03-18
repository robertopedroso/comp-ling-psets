import csv
from collections import Counter

def read_dx1(infile, d):
	phonemes = Counter()

	dx1_reader = csv.reader(infile, delimiter=d)
	for row in dx1_reader:
		row_phonemes = row[2].split() if len(row) <= 3 else row[2:]
		phonemes.update(Counter(row_phonemes))

	return phonemes

def analyze_dx1(infile, d, outfile):
	phonemes = read_dx1(infile, d).most_common()
	total_occurrences = sum([f for p,f in phonemes])

	writer = csv.writer(outfile, delimiter=d)
	writer.writerow(['phoneme', 'freq', 'rfreq'])
	for phoneme, freq in phonemes:
		rfreq = freq / total_occurrences
		writer.writerow([phoneme, freq, rfreq])

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='Analyzes a dx1 file to determine phoneme frequency in a given language.')

	parser.add_argument('-d', '--delimiter', action='store', default='\t', help='delimiter used by the dx1 file')
	parser.add_argument('infile', type=argparse.FileType('r'), help='dx1 file to analyze')
	parser.add_argument('outfile', type=argparse.FileType('w'), help='name of output file')
	args = parser.parse_args()

	analyze_dx1(args.infile, args.delimiter, args.outfile)
