Example use:

`python main.py infile outfile`
`python main.py data/english-corpus.txt output.txt`

Notes:

1) Stop conditions for the EM loop are configurable, but by default the program
ends at either 100 iterations or when the probability difference < 0.0001 (epsilon)

2) For example output of log ratio of state probabilities, refer to any of the files
within 'results'

3) For the output of my 20 iterations searching for local maxima, refer to the files
within 'results'. For a summary of corpus probabilities in each iteration, refer
to the file 'local-maxima-data.txt' in this directory.

There appear to be local maxima around 0.019, 0.023, 0.026, and 0.033. The highest
corpus probability (0.04798) was seen

		To State: 0	To State: 1	
From State: 0	0.697011619	0.302988381	
From State: 1	0.6281133196	0.3718866804	

The program has a great deal of difficulty tweaking the transition parameters if
they are initiially very different. For example, in iteration 16:

    Initial:
                    To State: 0	To State: 1	
    From State: 0	0.2944202623	0.7055797377	
    From State: 1	0.0339668655	0.9660331345	

    Final:
                    To State: 0	To State: 1	
    From State: 0	0.5233811658	0.4766188342	
    From State: 1	0.025439959	0.974560041	

As you can see, the parameters from state 0 changed dramatically, while the
parameters from state 1 barely shifted. Looking at the data, I made 3 observations:

(a) When the gap was smaller, transmission parameters tended to approach (0.5, 0.5).
(b) When state i -> 0 parameters were much larger than state i -> 1 parameters, the final transition parameters approached (1, 0).
(c) When state i -> 0 parameters were much smaller than i -> state 1 parameters, the final
transition parameters approached (0, 1).

Ultimately, based on the total corpus probability, the parameters should be around the
results from iteration 20:

		To State: 0	To State: 1	
From State: 0	0.697011619	0.302988381	
From State: 1	0.6281133196	0.3718866804	


4) For example output of viterbi paths, please refer to 'viterbi-paths-output.txt'
