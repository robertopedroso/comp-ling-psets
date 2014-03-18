from collections import Counter
from pylab import plot, savefig
import csv

def read_dx1(infile, d):
    '''Reads a dx1 file into a list of word phonemes.'''
    dx1_reader = csv.reader(infile, delimiter=d)
    return [(row[2].split() if len(row) <= 3 else row[2:]) for row in dx1_reader]

def compute_unigram_frequencies(phoneme_counter):
    '''
    Given a Counter object mapping unique phonemes to their total number of
    occurences in a corpus, produce a dict mapping unique phonemes to their
    unigram frequency with respect to that corpus.
    '''
    total_count = sum(phoneme_counter.values())

    symbol_frequencies = {}
    for symbol, count in phoneme_counter.items():
        symbol_frequencies[symbol] = float(count) / float(total_count)

    return symbol_frequencies

def sum_probabilities(i, alphabet, p):
    '''Returns the sum of empirical frequencies smaller than i.'''
    return sum(p[alphabet[j]] for j in xrange(1, i-1))

def compute_subinterval(i, alphabet, p):
    '''
    Maps a corpus symbol to a subinterval of [0,1) whose width is the letter's
    frequency and which partitions that interval. The interval is stored
    as a tuple.
    '''
    sum_p = sum_probabilities(i, alphabet, p)
    return (sum_p, sum_p + p[alphabet[i]])

def compute_interval(word, symbol_intervals, ltr=True):
    '''
    Iterates through a word and assigns it an interval.

    If ltr is True, the function will iterate from left to right over the word.
    If ltr is False, the function will iterate from right to left over the word.
    '''
    iterable = xrange(len(word)-1) if ltr else xrange(len(word)-2, -1, -1)

    low, high = 0.0, 1.0
    for i in iterable:
        symbol = word[i]
        code_range = high - low
        high = low + code_range * symbol_intervals[symbol][1]
        low = low + code_range * symbol_intervals[symbol][0]

    return (low, high)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-d', '--delimiter', action='store', default='\t', help='')
    parser.add_argument('infile', type=argparse.FileType('r'), help='')
    parser.add_argument('outfile', type=argparse.FileType('w'), help='')
    parser.add_argument('plotfile', type=str, help='')
    args = parser.parse_args()
    
    # get a list of words from the provided dx1 file
    words = read_dx1(args.infile, args.delimiter)

    # from the word list, get a list of phonemes and the sum of their
    # occurences in the given corpus
    phonemes = Counter()
    for word in words:
        phonemes.update(Counter(word))

    # given the list of phonemes and phoneme counts, compute the 
    # unigram frequency of each symbol in our corpus
    symbol_freqs = compute_unigram_frequencies(phonemes)

    # by sorting the list of symbols, we can get a sorted alphabet
    # a sortd alphabet allows us to speak of an n'th symbol
    alphabet = sorted(phonemes.keys())

    # map symbols to their computed intervals
    symbol_intervals = {}
    for i, letter in enumerate(alphabet):
        symbol_intervals[letter] = compute_subinterval(i, alphabet, symbol_freqs)

    # Iterate over the alphabetized list of words, compute its ltr and rtl
    # intervals, compute its probability and write this data to the outfile.
    # In the process, save tuples of (ltr_interval[0], rtl_interval[0]).
    points = []
    for word in sorted(words):
        ltr_interval = compute_interval(word, symbol_intervals)
        rtl_interval = compute_interval(word, symbol_intervals, ltr=False)
        points.append((ltr_interval[0], rtl_interval[0]))
        
        p1 = ltr_interval[1] - ltr_interval[0]
        p2 = rtl_interval[1] - rtl_interval[0]

        args.outfile.write('word: %s\n' % ''.join(word))
        args.outfile.write('  left-to-right probability: %s\n' % p1)
        args.outfile.write('  left-to-right interval: [%s, %s)\n' % \
                (ltr_interval[0], ltr_interval[1]))
        args.outfile.write('  right-to-left probability: %s\n' % p1)
        args.outfile.write('  right-to-left interval: [%s, %s)\n\n' % \
                (rtl_interval[0], rtl_interval[1]))

    # finally we plot our points and save the graph
    for x, y in points:
        plot(x, y, '+')

    savefig(args.plotfile)
