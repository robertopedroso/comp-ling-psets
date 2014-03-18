Please refer to output.txt for my program's (morphology.py in the code directory)
output. That file was produced by unning morphology.py on the basque.dx1 file I
generated for HW-1.

I was unable to test this program on EnglishSmall.dx1 because the runtime
complexity of this assignment was simply too much for my Macbook Air's
Core i3 CPU to handle. I gave up after 45 minutes of attempted computation.
Unfortunately, computing the requested operations on 13,000 words yields something
like 84,500,000 pairs. I'm confident the program would have worked, based on various
tests and the output from basque.dx1.

Command syntax:

python morphology.py infile.dx1 -d ' ' outfile.txt -m 

The -d flag denotes your dx1 file delimiter (defaults to \t) and -m will cause
the program to write an alphabetized list of words that belong to two different
signatures (as per #7) to stdout.

The content of output.txt matches the formatting expected from the problem set.
As #6 requests, the output is sorted with respect to how many word-pairs fell
under each signature. Since direction was not specified, the tables are ordered
from largest to smallest. I also impemented prefix/suffix detection in the 
table headers, denoted by (prefix) or (suffix) after the signature.

Linguistically, signature tables are interesting because they can help
identify stems, affixes, other forms of declension, etc.

There are various reasons the program might assign the same word to multiple
signatures, but the most common case is when one word is a stem and there are
multiple possible affixes. For example, 'walk' is an English morpheme which can
take the affix 'ing' to become 'walking', 'ed' to become 'walked', 's' to become
'walks', and so forth. 
