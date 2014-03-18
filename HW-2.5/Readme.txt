There is not much to say here. The results of the assignment, as per what
was asked for in part (4), can be found in the file 'output.txt' in this
directory. The code which produced this output can be found in the 'code'
directory.

The format of 'output.txt' is a list of anagrams preceded by a parenthetical
note. The paranthetical note takes the form:

(letters, anagram size, anagram length)

where anagram size and length are defined by the problem set document. This
note is added primarily to help validate that the list of anagrams
is sorted properly.

Due to lack of time, I did not attempt part (5) - the extra credit problem.
My first intuition was that such a function would be trivial: the bulk of
low-quality anagram sets in the assignment PDF were the result of possessive
marks and pluralization. When you look at dict.txt, however, there are no
apostrophes to be found, and a cursory examination of output.txt suggests that 
pluralization is not as prevalent as possible.

There are two improvements to such a function that could be made in order
to identify quality anagrams.

(1) Eliminating anagram sets resulting from typos. There are surprisingly
many of these cases. I theorize that the simplest way to eliminate typos is
to cross-check words from the input file against a well-edited corpus, for
example, a dictionary.

(2) Using fuzzy string matching. In many cases, we find lame anagrams like
"redecect" and "detector", or "theology" and "ethology". These anagrams
are not as interesting as "creationism" and "anisometric" because they contain
identical substrings or share other spelling patterns.

You could exclude many of these cases by computing their Levenshtein distance
and comparing that distance to some minimal threshold. Words below that
threshold would be excluded for being too similar while words that exceed
the threshold would potentially make for more interesting anagrams. In addition
to Levensthein distance, you could perform some kind of substring detection for
those cases where very long words containing the same substring have a greater
Levenshtein distance than two smaller but more interesting words.
