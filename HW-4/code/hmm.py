import numpy as np

class HiddenMarkovModel(object):
    def __init__(self, n, alphabet, A=None, B=None, pi=None, precision=np.double):
        self.n = n
        self.alphabet = alphabet
        self.precision = precision

        self.A = A if A else self._randomize_A()
        self.B = B if B else self._randomize_B()
        self.pi = pi if pi else self._randomize_pi()

    def _randomize_A(self):
        '''Generates random transition probabilities, normalized to 1.'''
        return np.array([np.random.dirichlet(np.ones(self.n, dtype=self.precision), size=1)[0] for i in xrange(self.n)])

    def _randomize_B(self):
        '''Generates random emission probabilities, normalized to 1.'''
        return np.array([np.random.dirichlet(np.ones(len(self.alphabet), dtype=self.precision), size=1)[0] for i in xrange(self.n)])

    def _randomize_pi(self):
        '''Generates random pi values, normalized to 1.'''
        return np.random.dirichlet(np.ones(self.n, dtype=self.precision), size=1)[0]

    def compute_total_probability(self, alpha, beta):
        '''Computes the total probability of an observation.'''
        total = 0.0

        for i in xrange(self.n):
            total += alpha[0][i] * beta[0][i]

        return total

    def _calcalpha(self, observation):
        def recursive_alpha(i, t, o):
            if t == 0:
                return self.pi[i]
            else:
                return sum(recursive_alpha(j, t-1, o) * self.A[j][i] * self.B[j][self.alphabet.index(o[t-1])] for j in xrange(self.n))

        alpha = np.zeros((len(observation)+1, self.n), dtype=self.precision)

        for t in xrange(len(observation)+1):
            for i in xrange(self.n):
                alpha[t][i] = recursive_alpha(i, t, observation)

        return alpha

    def _calcbeta(self, observation):
        def recursive_beta(i, t, o):
            if t == len(o):
                return 1
            else:
                return sum(recursive_beta(j, t+1, o) * self.A[i][j] * self.B[i][self.alphabet.index(o[t])] for j in xrange(self.n))

        beta = np.zeros((len(observation)+1, self.n), dtype=self.precision)

        for t in xrange(len(observation), -1, -1):
            for i in xrange(self.n):
                beta[t][i] = recursive_beta(i, t, observation)

        return beta

    def softcount_table(self, word, p):
        sc_table = {letter: np.zeros((self.n, self.n), dtype=self.precision) for letter in self.alphabet}

        for t, letter in enumerate(word):
            for i in xrange(self.n):
                for j in xrange(self.n):
                    sc_table[letter][i][j] += p[t][i][j]

        return sc_table

    def _calcsoftcounts(self, observation, alpha=None, beta=None):
        if alpha is None:
            alpha = self._calcalpha(observation)

        if beta is None:
            beta = self._calcbeta(observation)

        p = np.zeros((len(observation), self.n, self.n), dtype=self.precision)

        for t in xrange(len(observation)):
            p_O = self.compute_total_probability(alpha, beta)

            for i in xrange(self.n):
                for j in xrange(self.n):
                    topterms = np.zeros(4, dtype=self.precision)
                    topterms[0] = alpha[t][i]
                    topterms[1] = self.A[i][j]
                    topterms[2] = self.B[i][self.alphabet.index(observation[t])]
                    topterms[3] = beta[t+1][j]

                    p[t][i][j] = np.prod(topterms) / p_O

        return p, alpha, beta
    
    def reestimateA(self, ec):
        new_A = np.zeros((self.n, self.n), dtype=self.precision)

        for i in xrange(self.n):
            for j in xrange(self.n):
                numer, denom = 0.0, 0.0

                for letter, p in ec.items():
                    numer += p[i][j]    
                    denom += np.sum(p[i]) 

                new_A[i][j] = numer / denom
        
        return new_A

    def reestimateB(self, ec):
        new_B = np.zeros((self.n, len(self.alphabet)), dtype=self.precision)

        for i in xrange(self.n):
            for letter, p in ec.items():
                numer, denom = 0.0, 0.0

                for j in xrange(self.n):
                    numer += p[i][j]

                for m in self.alphabet:
                    for j in xrange(self.n):
                        denom += ec[m][i][j]

                new_B[i][self.alphabet.index(letter)] = numer / denom

        return new_B

    def reestimatepi(self, ic, numwords):
        new_pi = np.zeros(self.n, dtype=self.precision)

        for i in xrange(self.n):
            numer = 0.0

            for letter in self.alphabet:
                for j in xrange(self.n):
                    numer += ic[letter][i][j]

            new_pi[i] = numer / numwords

        return new_pi

    def maximize(self, words):
        '''A single iteration of the Expectation-Maximization procedure'''
        sc = {l: np.zeros((self.n, self.n), dtype=self.precision) for l in self.alphabet}
        isc = {l: np.zeros((self.n, self.n), dtype=self.precision) for l in self.alphabet}
        words_p = 0.0

        for n, word in enumerate(words):
            soft_counts, alpha, beta = self._calcsoftcounts(word)

            # Initial counts
            for i in xrange(self.n):
                for j in xrange(self.n):
                    l = word[0]
                    isc[l][i][j] += soft_counts[0][i][j]

            # expected counts tallying
            sc_table = self.softcount_table(word, soft_counts)

            for letter, p in sc_table.items():
                for i in xrange(self.n):
                    for j in xrange(self.n):
                        sc[letter][i][j] += p[i][j]

            # collect word probabilities
            words_p += self.compute_total_probability(alpha, beta)

        self.A = self.reestimateA(sc)
        self.B = self.reestimateB(sc)
        self.pi = self.reestimatepi(isc, len(words))

        return words_p

    def train(self, words, iterations=100, epsilon=0.0001, verbose=False):
        '''
        Trains HMM paramaters on a given list of words.

        The training loop repeats until either:
        (1) it reaches the iteration limit parameter
        (2) the sum of word probabilities changes less than epsilon
        '''
        previous_probability = 0.0

        for i in xrange(iterations):
            probability = self.maximize(words)

            if verbose:
                print "Iteration: %s\tPrevious Probability: %s\tCurrent Probability: %s" % \
                    (i, previous_probability, probability)

            if abs(probability - previous_probability) < epsilon:
                if verbose:
                    print "Final probability: %s" % probability
                break
            else:
                previous_probability = probability
        else:
            print "Final probability: %s" % probability

    def viterbi(self, word):
        '''Finds the best path through the HMM to generate a given word.'''
        wordlen = len(word)
        delta = np.zeros((wordlen, self.n), dtype=self.precision)
        psi = np.zeros((wordlen, self.n), dtype=self.precision)

        # initialization step
        for i in xrange(self.n):
            delta[0][i] = self.pi[i] * self.B[i][0]

        # induction and backtrace
        for t in xrange(1, wordlen):
            for j in xrange(self.n):
                for i in xrange(self.n):
                    possible = delta[t-1][i] * self.A[i][j]

                    if delta[t][j] < possible:
                        delta[t][j] = possible
                        psi[t][j] = i

                delta[t][j] *= self.B[j][self.alphabet.index(word[t])]

        # termination and path readout
        max_p = 0
        path = np.zeros(wordlen, dtype=self.precision)
        for i in xrange(self.n):
            possible = delta[wordlen-1][i]

            if max_p < possible:
                max_p = possible
                path[wordlen-1] = i

        for i in xrange(1, wordlen):
            path[wordlen-i-1] = psi[wordlen-i][path[wordlen-i]]
        
        return path
