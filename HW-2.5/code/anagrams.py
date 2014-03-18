def get_dx1_words(fname, minletters):
    with open(fname, 'rb') as f:
        return [word.strip() for word in f if len(word.strip()) >= minletters]

def sort_word(word):
    return ''.join(sorted(word))

def get_sorted_words(words):
    return {word: sort_word(word) for word in words}

def sort_anagrams(anagrams):
    # https://stackoverflow.com/questions/7742752/sorting-a-dictionary-by-value-then-by-key
    # ^ credit where it is due, I knew about the sorted() lambda idiom, but I did not 
    # realize I could use a tuple in the key lambda to fine-tune the sorting
    return sorted(anagrams.items(), key=lambda tup: (len(tup[1]), len(tup[0])))

def get_anagrams(words):
    sorted_words = get_sorted_words(words)
    anagrams = {}

    for word, sorted_word in sorted_words.iteritems():
        if sorted_word in anagrams:
            if word not in anagrams[sorted_word]:
                anagrams[sorted_word].append(word)
        else:
            anagrams[sorted_word] = [word]

    # get rid of sorted words with only one word (they're not anagrams)
    clean_anagrams = {sw: words for sw, words in anagrams.iteritems() if len(words) > 1}
    return sort_anagrams(clean_anagrams)

if __name__ == "__main__":
    words = get_dx1_words('dict.txt', 8)
    anagrams = get_anagrams(words)

    with open('output.txt', 'w') as f:
        for letters, al in anagrams:
            f.write("(%s, %s, %s) %s\n" % (letters, len(al[1]), len(al[0]), ', '.join(al)))
