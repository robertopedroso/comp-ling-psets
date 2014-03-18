import numpy as np

class HiddenMarkovModel(object):
    def __init__(self, n, alphabet, A, B, pi, precision=np.double):
        self.n = n
        self.alphabet = alphabet
        self.precision = precision

        self.A = A
        self.B = B
        self.pi = pi

    def forward(self, observation):
        '''This is just a public wrapper function for testing purposes.'''
        return self._calcalpha(observation)

    def backward(self, observation):
        '''This is just a public wrapper function for testing purposes.'''
        return self._calcbeta(observation)

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

    def getsoftcounts(self, observation, alpha=None, beta=None):
        '''Wrapper function for testing _calcp'''
        return self._calcsoftcounts(observation, alpha, beta)

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

        return p
    
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
