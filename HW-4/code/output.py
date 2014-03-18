import numpy as np

def dump_state(f, hmm, init_msg):
    f.write('-------------------------------------------------------------------------\n')
    f.write('-  %s\n' % init_msg)
    f.write('-------------------------------------------------------------------------\n')
    
    f.write('\n---------------------------------\n')
    f.write('Pi Values:\n')
    
    for i in xrange(hmm.n):
        f.write('State\t%s\t%s\n' % (i, hmm.pi[i]))

    f.write('\n')
    f.write('---------------------------------\n')
    f.write('-  Emission Probabilities       -\n')
    f.write('---------------------------------\n')

    for i in xrange(hmm.n):
        f.write('\tState %s\t' % i)
    f.write('\n')

    for t, letter in enumerate(hmm.alphabet):
        f.write('  %s\t' % letter)

        for i in xrange(hmm.n):
            f.write('%s\t' % np.round(hmm.B[i][t], 12))

        f.write('\n')

    f.write('\n')
    f.write('Log ratios of emissions from the 2 states:\n')

    # Calculate and sort log ratios on the fly
    log_ratios = {}
    for t, letter in enumerate(hmm.alphabet):
        log_ratios[letter] = np.log2(hmm.B[0][t] / hmm.B[1][t])

    for letter, log_ratio in sorted(log_ratios.items(), key=lambda x: x[1], reverse=True):
        f.write('  %s\t%s\n' % (letter, log_ratio))

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
            f.write('%s\t' % np.round(hmm.A[j][i], 10))
        f.write('\n')

    f.write('\n\n')

def viterbi_output(f, word_paths):
    f.write('---------------------------------\n')
    f.write('-  Viterbi Paths                -\n')
    f.write('---------------------------------\n')

    for word, path in word_paths.items():
        f.write('Best path for: %s\n' % word)

        f.write('time:')
        for t in xrange(len(word)):
            f.write('\t%s' % t)
        f.write('\n')

        f.write('state:')
        for t in xrange(len(word)):
            f.write('\t%s' % int(path[t]))
        f.write('\n\n')
