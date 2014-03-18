Language of Choice: Basque

For code, refer to the ./code directory. You can look at the README.md file
there or at: https://github.com/robertopedroso/basque-dx1-generator

The README.md file gives example commands but you can clarificaiton on
all available parameters and flags by executing any file with the flag -h.

For phoneme analyses of basque and other .dx1 files, refer to the directory
called ./phoneme-analyses.

The corpus, available in ./code/sources, was a Basque translation of the
New Testament, which can be found here: http://www.sacred-texts.com/bib/wb/bsq/

The code is written to work in Python 3 because of UTF-8 compatibility. Basque
employs many latin characters and UTF-8 was the simplest way of dealing with
strange characters. The code can *probably* be made functional in python 2.7
by adding the following lines at the top of the files:

#!/usr/bin/env python
# -*- coding: utf-8 -*- 

The file dx1-generator.py also requires Matthew Barnett's regex module:

https://pypi.python.org/pypi/regex

The standard Python re module has poor unicode support whereas Matthew's
regex library supports operations from the unicoe specification like 
\p{alpha} to match any valid UTF-8 letter from any alphabet. 

Other than UTF-8 issues, generating and analyzing DX1 files from sources was trivial.
The most significant problem was in producing phonetic transcriptions of known Basque
words. I looked into many options, including scraping online Basque dictionaries or
exploiting existing Basque TTS libraries, but no option was consistent.

Instead, I buckled down and wrote out transcription rules for as much of the Basque
language as I could figure out via Google search. In several cases I even researched
and implemented workarounds for phonological rules and weird edge cases. I'm fairly
satisfied that my dictionary's pronunciations are at least somewhat close to Basque.
