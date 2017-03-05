import scipy.stats as sp
import re
from operator import itemgetter
from collections import OrderedDict
from collections import Counter

## This method returns the most likely correct spelling of a misspelled word
def correction(word):

	candidate_stats = get_candidate_stats(candidates(word), word)

	min_stat = candidate_stats[candidate_stats.keys()[0]]

	tied = {}

	for i in range(0, len(candidate_stats.keys())):
		if candidate_stats[candidate_stats.keys()[i]] == min_stat:
			tied.update({candidate_stats.keys()[i]: P(candidate_stats.keys()[i])})
		else:
			break 

	tied_sorted = OrderedDict(sorted(tied.items()), key=itemgetter(1))

	return tied_sorted.keys()[0]

def get_candidate_stats(candidates, target):
	candidate_stats = {}
	target_freq = get_letter_freq(target).values()
	for candidate in candidates:
		candidate_freq = get_letter_freq(candidate).values()

		stat, pval = sp.stats.chisquare(target_freq, candidate_freq)
		candidate_stats.update({candidate: stat})

	return OrderedDict(sorted(candidate_stats.items(), key=itemgetter(1)))

def get_letter_freq(word):
	freq = {"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 1,
	         "i": 1, "j": 1, "k": 1, "l": 1, "m": 1, "n": 1, "o": 1, "p": 1,
	         "q": 1, "r": 1, "s": 1, "t": 1, "u": 1, "v": 1, "w": 1, "x": 1,
	         "y": 1, "z": 1}
	for letter in word:
		if letter in "abcdefghijklmnopqrstuvwxyz":
			freq[letter] += 1
	
	return freq
	
############################## BEGIN NORVIG'S CODE ############################
def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))
## Added to support a different dictionary
# DICT = Counter(words(open('dictionary.txt').read()))

def norv_correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

## DICT originally read WORDS but we wanted to make this compatible with
## a different dictionary
def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))