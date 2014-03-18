from collections import Counter
from itertools import combinations
import csv
import re

def prettify(ctr):
    return ''.join(sorted(ctr.elements()))

def analyze_word_pair(m, n):
    m, n = Counter(m), Counter(n)

    stem = m & n
    maffix = m - stem
    naffix = n - stem

    return (prettify(stem), maffix, naffix)

def find_pairs_of_words(w1, w2, min_stem_length=4, max_affix=4):
    stem, maffix, naffix = analyze_word_pair(w1, w2)
    if not maffix:
        maffix = ''

    if not naffix:
        naffix = ''

    if maffix != '':
        maffix = prettify(maffix)

    if naffix != '':
        naffix = prettify(naffix)

    if len(stem) < min_stem_length:
        return False
    
    if len(maffix) > max_affix or len(naffix) > max_affix:
        return False

    return (w1, w2, stem, maffix, naffix, maffix+ '_' +naffix)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('infile', type=argparse.FileType('r'), help='')
    parser.add_argument('-d', '--delimiter', action='store', default='\t', help='')
    parser.add_argument('outfile', type=argparse.FileType('w'), help='')
    parser.add_argument('-m', '--multiples', action='store_true', help='')
    args = parser.parse_args()

    reader = csv.reader(args.infile, delimiter=args.delimiter)
    words = [row[0] for row in reader]

    pairs = []
    for pair in combinations(words, 2):
        result = find_pairs_of_words(pair[0], pair[1])
        if result: pairs.append(result)

    # get list of unordered signatures which occur >= 10 times
    sigs = Counter(tup[5] for tup in pairs)
    big_sigs = [k for k, v in sigs.items() if v >= 10]

    # create a dict of big_sigs mapped to lists of matching tuples
    sig_tables = {}
    for pair in pairs:
        if pair[5] in big_sigs:
            if pair[5] in sig_tables.keys():
                sig_tables[pair[5]].append(pair)
            else:
                sig_tables[pair[5]] = [pair]

    sorted_sig_tables = sorted(sig_tables.items(), key=lambda tup: (len(tup[1]), tup[0]), reverse=True)
    for sig, sigpairs in sorted_sig_tables:
        # write table heading
        args.outfile.write('-'*50 + '\n')
        if re.match(r'^_.+$', sig):
            args.outfile.write('%s (suffix)\n' % sig)
        elif re.match(r'^.+_$', sig):
            args.outfile.write('%s (prefix)\n' % sig)
        else:
            args.outfile.write('%s\n' % sig)
        args.outfile.write('-'*50 + '\n')

        # write table rows
        for pair in sigpairs:
            args.outfile.write('%s %s\n' % (pair[0], pair[1]))

        # write a newline for neatness
        args.outfile.write('\n')

    if args.multiples:
        possible_dups = []
        for _, sigpairs in sig_tables.iteritems():
            for pair in sigpairs:
                possible_dups.append(pair[0])
                possible_dups.append(pair[1])

        counted_dups = Counter(possible_dups)
        dups = [dup for dup, count in counted_dups.items() if count > 1]

        dups.sort()
        for dup in dups:
            print dup

