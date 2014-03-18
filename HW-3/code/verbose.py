import numpy as np

def initialization(f, n, alphabet, A, B, pi):
    f.write('---------------------------------\n')
    f.write('-  Initialization               -\n')
    f.write('---------------------------------\n')

    for i in xrange(n):
        f.write('Creating state %s\n' % i)

        f.write('Transitions\n')
        for j in xrange(n):
            f.write('\tTo state\t%s\t%s\n' % (j, A[i][j]))

        f.write('\nEmission Probabilities\n')
        for t, l in enumerate(alphabet):
            f.write('\tLetter\t%s\t%s\n' % (l, B[i][t]))

    f.write('\n\n')
    f.write('---------------------------\n')

    f.write('Pi:\n')
    for i in xrange(n):
        f.write('State\t%s\t%s' % (i, pi[i]))

def forwardbackward(f, hmm, words):
    f.write('\n\n')
    f.write('---------------------------------\n')
    f.write('-  Iteration Number 0           -\n')
    f.write('---------------------------------\n')

    for word in words:
        f.write('\n')
        f.write('*** word: %s ***' % word)
        f.write('\n')

        alpha = hmm.forward(word)
        beta = hmm.backward(word)

        f.write('Forward\n\n')
        for i in xrange(hmm.n):
            f.write('Pi of state\t%s\t%s\n' % (i, hmm.pi[i]))

        f.write('\n')
        for t, l in enumerate(word):
            f.write("Time %s: '%s'\n" % (t+2, l))

            for i in xrange(hmm.n):
                f.write('\tto state: %s\n' % i)

                for j in xrange(hmm.n):
                    f.write('\t\tfrom state\t%s\t' % j)

                    tmp = alpha[t][j] * hmm.A[j][i] * hmm.B[j][hmm.alphabet.index(l)]
                    f.write("previous Alpha time arc's a and b: %s\n" % (tmp))

                f.write('\n')
                f.write('\tAlpha at time = %s, state = %s: %s\n' % (t+2, i, alpha[t+1][i]))
                f.write('\n')

            f.write("\tSum of alpha's at time = %s: %s\n" % (t+2, np.sum(alpha[t+1])))
            f.write('\n')

        f.write('Alpha:\n\n')
        for t in xrange(len(word)+1):
            f.write('Time\t%s\tState\t0:\t%s\tState\t1:\t%s\n' % (t+1, alpha[t][0], alpha[t][1]))

        f.write('\nBeta:\n\n')
        for t in xrange(len(word)+1):
            f.write('Time\t%s\tState\t0:\t%s\tState\t1:\t%s\n' % (t+1, beta[t][0], beta[t][1]))

def total_probability(f, hmm, words):
    f.write('\n')
    f.write('---------------------------------\n')
    f.write('-  Total Probabilities          -\n')
    f.write('---------------------------------\n')

    for word in words:
        alpha = hmm.forward(word)
        beta = hmm.backward(word)
        p_O = hmm.compute_total_probability(alpha, beta)

        f.write("Total probability of '%s': %s\n" % (word, p_O))

def soft_counts(f, hmm, words):
    f.write('\n')
    f.write('---------------------------------\n')
    f.write('-  Soft Counts                  -\n')
    f.write('---------------------------------\n')

    expected_counts = {letter: np.zeros((hmm.n, hmm.n), dtype=hmm.precision) for letter in hmm.alphabet}
    initial_counts = {letter: np.zeros((hmm.n, hmm.n), dtype=hmm.precision) for letter in hmm.alphabet}

    for word in words:
        f.write('\n')
        f.write('*** word: %s ***' % word)
        f.write('\n')

        f.write('\nAs soft counts, they should add up to 1.0 for each letter emitted.\n')
        f.write('\n')

        soft_counts = hmm.getsoftcounts(word)

        for t, letter in enumerate(word):
            f.write('\nLetter: %s\n' % letter)

            for i in xrange(hmm.n):
                f.write('\tFrom state: %s\n' % i)

                for j in xrange(hmm.n):
                    f.write('\t\tto state:\t%s\t%s;\n' % (j, soft_counts[t][i][j]))

                    if t == 0:
                        initial_counts[letter][i][j] += soft_counts[t][i][j]

        # expected counts tally
        sc_table = hmm.softcount_table(word, soft_counts)

        for letter, p in sc_table.items():
            for i in xrange(hmm.n):
                for j in xrange(hmm.n):
                    expected_counts[letter][i][j] += p[i][j]

        if word == words[-1]:
            f.write('\nExpected counts table (final)\n')
        else:
            f.write('\nExpected counts table (so far)\n')

        for letter, p in expected_counts.items():
            for i in xrange(hmm.n):
                for j in xrange(hmm.n):
                    f.write('\t%s\t%s\t%s\t%s\n' % (letter, i, j, p[i][j]))
    
    return expected_counts, initial_counts

def maximization(f, hmm, expected_counts, initial_counts, numwords):
    f.write('\n')
    f.write('---------------------------------\n')
    f.write('-  Maximization                 -\n')
    f.write('---------------------------------\n')
    f.write('Transition Probabilities\n')

    new_A = hmm.reestimateA(expected_counts)

    for i in xrange(hmm.n):
        f.write('\nFrom State: %s\n' % i)

        for j in xrange(hmm.n):
            f.write('\tto state: %s\tprob: %s\n' % (j, new_A[i][j]))

    new_B = hmm.reestimateB(expected_counts)

    f.write('\n\nEmission Probabilities\n')

    for i in xrange(hmm.n):
        f.write('\nFrom State: %s\n' % i)

        for letter, p in expected_counts.items():
            f.write('\tletter: %s\n' % letter)

            for j in xrange(hmm.n):
                f.write('\t\tto state\t%s\t%s\n' % (j, p[i][j]))

            f.write("\t\tTotal soft count of '%s' from state = %s equals: %s\n\n" % (letter, i, np.sum(p[i])))

        f.write('\tNormalize soft counts to get emission probabilities:\n')
        for k, letter in enumerate(hmm.alphabet):
            f.write('\t\tletter: %s\tprobability: %s\n' % (letter, new_B[i][k]))

    new_pi = hmm.reestimatepi(initial_counts, numwords)

    f.write('\n\n')
    f.write('-------------------------------------------------------------------------\n')
    f.write('-  End of iteration summary                                             -\n')
    f.write('-------------------------------------------------------------------------\n')
    
    f.write('\n---------------------------------\n')
    f.write('Pi Values:\n')
    
    for i in xrange(hmm.n):
        f.write('State\t%s\t%s\n' % (i, new_pi[i]))

    f.write('\n')
    f.write('---------------------------------\n')
    f.write('-  Emission Probabilities       -\n')
    f.write('---------------------------------\n')

    for i in xrange(hmm.n):
        f.write('\tState %s\t' % i)
    f.write('\n')

    for t, letter in enumerate(hmm.alphabet):
        f.write(letter)

        for i in xrange(hmm.n):
            f.write('\t%s' % new_B[i][t])

        f.write('\n')

    f.write('\n')
    f.write('---------------------------------\n')
    f.write('-  Transition Probabilities     -\n')
    f.write('---------------------------------\n')
    
    f.write('\t\t')
    for i in xrange(hmm.n):
        f.write('To State: %s\t' % i)
    f.write('\n')

    for j in xrange(hmm.n):
        f.write('From State: %s\t' % j)

        for i in xrange(hmm.n):
            f.write('%s\t' % new_A[i][j])
        f.write('\n')
