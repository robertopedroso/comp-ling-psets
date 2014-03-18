from hmm import HiddenMarkovModel
from output import dump_state, viterbi_output
import numpy as np

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-d', '--dev', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-n', '--numstates', type=int, default=2)
    parser.add_argument('-m', '--mode', type=str, default='loop')
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('outfile', type=argparse.FileType('w'))
    args = parser.parse_args()

    # overwrite the numstates arg for our purposes...
    # numstates = argparse.numstates
    numstates = 2

    # pull words from corpus, strip newline, append '#'
    words = [word.rstrip() + '#' for word in args.infile.readlines()]

    # compute the alphabet from the dataset
    alphabet = ''.join(set(''.join(words)))

    # use testing parameters in dev mode
    if args.dev:
        alphabet = 'abdi#'
        words = ['babi#', 'dida#']

    # for #3, we run the training program 20 times to look for local maxima
    if args.mode == 'loop':
        print "Beginning iteration for Local Maxima question..."

        for i in xrange(1, 21):
            print "Local Maxima question: iteration %s" % i

            outfile = open('results/result%s.txt' % i, 'w')

            hmm = HiddenMarkovModel(numstates, alphabet)
            dump_state(outfile, hmm, 'Initial State')

            hmm.train(words, iterations=100, verbose=args.verbose)
            dump_state(outfile, hmm, 'Iteration Summary')

        print "Completed Local Maxima question."

    # for #4 we train and then compute the viterbi path for each word
    # we store each word-path pair in a dict and then pass that dict
    # to a function that handles output
    if args.mode == 'viterbi':
        hmm = HiddenMarkovModel(numstates, alphabet)
        dump_state(args.outfile, hmm, 'Initial State')

        hmm.train(words, iterations=100, verbose=args.verbose)
        dump_state(args.outfile, hmm, 'Iteration Summary')

        word_paths = {}
        for word in words:
            word_paths[word] = hmm.viterbi(word)

        viterbi_output(args.outfile, word_paths)
