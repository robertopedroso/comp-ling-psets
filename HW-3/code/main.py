from hmm import HiddenMarkovModel
import numpy as np
import verbose

if __name__ == "__main__":
    outfile = open('output.txt', 'w')

    numstates = 2
    alphabet = 'abdi#'
    words = ['babi#', 'dida#']

    A = np.array([[0.5000, 0.5000], [0.5000, 0.5000]])
    B = np.array([[0.2141, 0.3181, 0.2486, 0.0156, 0.2035],
        [0.1197, 0.0504, 0.2821, 0.2610, 0.2868]])
    pi = np.array([0.3196, 0.6804])
   
    # Initialization step
    verbose.initialization(outfile, numstates, alphabet, A, B, pi)
    hmm = HiddenMarkovModel(numstates, alphabet, A, B, pi)

    # Forward-Backward test
    verbose.forwardbackward(outfile, hmm, words)

    # Total Probabilities
    verbose.total_probability(outfile, hmm, words)

    # Soft Counts
    ec, ic = verbose.soft_counts(outfile, hmm, words)

    # Maximization
    verbose.maximization(outfile, hmm, ec, ic, len(words))
