'''

This file is intended to determine the number of rounds necessary to guarantee 
that the guesser wins.

Using the current process in worst_case_for_one(), it is possible to miss the 
hardest-to-guess word. However, it provides a lower bound on how many guesses 
the guesser must make to be guaranteed to win.

count for a: 4891 because of ^[^a][^a][^a][^a][^a][^a][^a]$
count for b: 7775 because of ^[^b][^b][^b][^b][^b][^b][^b][^b]$
count for c: 6692 because of ^[^c][^c][^c][^c][^c][^c][^c]$
count for d: 6333 because of ^[^d][^d][^d][^d][^d][^d][^d][^d]$
count for e: 2778 because of ^[^e][^e][^e][^e][^e][^e][^e][^e]$

count for f: 8152 because of ^[^f][^f][^f][^f][^f][^f][^f][^f]$
count for g: 6785 because of ^[^g][^g][^g][^g][^g][^g][^g][^g]$
count for h: 7516 because of ^[^h][^h][^h][^h][^h][^h][^h][^h]$
count for i: 4506 because of ^[^i][^i][^i][^i][^i][^i][^i]$
count for j: 8986 because of ^[^j][^j][^j][^j][^j][^j][^j][^j]$
count for k: 8326 because of ^[^k][^k][^k][^k][^k][^k][^k][^k]$
count for l: 5769 because of ^[^l][^l][^l][^l][^l][^l][^l][^l]$
count for m: 7441 because of ^[^m][^m][^m][^m][^m][^m][^m][^m]$

count for n: 5250 because of ^[^n][^n][^n][^n][^n][^n][^n]$
count for o: 5932 because of ^[^o][^o][^o][^o][^o][^o][^o]$
count for p: 7358 because of ^[^p][^p][^p][^p][^p][^p][^p][^p]$
count for q: 8966 because of ^[^q][^q][^q][^q][^q][^q][^q][^q]$
count for r: 4645 because of ^[^r][^r][^r][^r][^r][^r][^r]$
count for s: 4095 because of ^[^s][^s][^s][^s][^s][^s][^s]$

count for t: 5528 because of ^[^t][^t][^t][^t][^t][^t][^t]$
count for u: 6782 because of ^[^u][^u][^u][^u][^u][^u][^u][^u]$
count for v: 8428 because of ^[^v][^v][^v][^v][^v][^v][^v][^v]$
count for w: 8347 because of ^[^w][^w][^w][^w][^w][^w][^w][^w]$
count for x: 8953 because of ^[^x][^x][^x][^x][^x][^x][^x][^x]$
count for y: 8132 because of ^[^y][^y][^y][^y][^y][^y][^y][^y]$
count for z: 9000 because of ^[^z][^z][^z][^z][^z][^z][^z][^z]$

'''

import WordList
import re

wl = WordList.WordList()

def worst_case():
	return worst_case_for_one('.')

def worst_case_for_one(regex):
	# Worst case for the first guess.
	
	words = [ word for word in wl.lines if re.search(regex, word) != None ]
	
	best_regex = None
	best_count = 0
	
	for c in range(ord('t'), ord('z')+1):
		regex, count = max_for_new_guess(words, str(chr(c)))
		print 'count for ' + str(chr(c)) + ': ' + str(count) + ' because of ' + regex
		if count > best_count:
			best_regex = regex
			best_count = count
	
	print best_regex, best_count


def max_for_new_guess(saved_words, guess):
	# Find the word that leaves the maximum number of possible results where it 
	# either does or does not contain the given guessed letter. If the
	# guessed letter does exist, check every possible position(s).
	
	best_regex = None
	best_count = 0
	words = [ word for word in saved_words ]
	
	for i in range(len(words)):
		if len(words[i]) == 0:
			continue
		count = 0
		regex = '^' # Matches words[i] and any other words like it.
		for c in words[i]:
			regex += guess if c == guess else '[^' + guess + ']'
		regex += '$'
		for j in range(i, len(words)):
			if re.search(regex, words[j]) != None:
				count += 1
				words[j] = ''
		if count > best_count:
			best_regex = regex
			best_count = count
	return (best_regex, best_count)

print worst_case()