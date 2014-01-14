'''
This is the actual guesser that gets run.
'''

import WordList

wordlist = WordList.WordList()

class Guesser:
	
	def __init__(self):
		self.vowel_match = '[aeiouy]'
		self.consonant_match = '[bcdfghjklmnpqrstvwxz]'
		
		self.wins = 0
		self.trials = 0
		
		self.frequency = wordlist.letter_frequency()
		self.vowel_frequency, self.consonant_frequency = self.vowel_consonant_frequency(self.frequency)
		
		# 1/3 and 1/4 are the best values I tried, depending on what executioner.count 
		# equals. 7/24 is right between 1/3 and 1/4.
		self.given_words_weights = [ [ i/24.0, 0, 1000.0 ] for i in range(3) ]
		
		# The default will be 7/24. But if it starts doing badly enough, 7/24's 
		# ratio will drop and the guesser will switch to a different weight.
		self.given_words_weights[0] = [ 7/24.0, 22, 12.0 ]
		self.given_words_weights[1] = [ 12/24.0, 18, 12.0 ]
		self.given_words_weights[2] = [ 18/24.0, 14, 12.0 ]
		self.given_words_weight = 7.0 / 24
		
		# Each new word will weigh into the given word frequency by this much. 
		# 1/30 is recommended.
		self.new_word_weight = 1.0 / 30
		
		self.given_frequency = {}
		for c in range(ord('a'), ord('z')+1):
			self.given_frequency[chr(c)] = 0
	
	def vowel_consonant_frequency(self, frequency):
		vowel_frequency = ''; consonant_frequency = ''
		vowels = WordList.re.findall(self.vowel_match, frequency)
		consonants = WordList.re.findall(self.consonant_match, frequency)
		for v in vowels:
			vowel_frequency += v
		for c in consonants:
			consonant_frequency += c
		return (vowel_frequency, consonant_frequency)
	
	def modify_frequency(self, finder=None):
		letters = wordlist.detailed_frequency(wordlist.find_words(finder))
		total_letter_freq = 0.0
		for k in letters:
			total_letter_freq += letters[k]
		
		total_given_freq = 0.0
		for k in self.given_frequency:
			total_given_freq += self.given_frequency[k]
		
		frequency_dict = {}
		for k in letters:
			if total_letter_freq != 0: # don't divide by 0
				frequency_dict[k] = (letters[k] * (1 - self.given_words_weight)) / total_letter_freq
			
		for k in self.given_frequency:
			if total_given_freq != 0: # don't divide by 0
				if frequency_dict[k] != 0: # if there are no possible combinations, don't bother increasing the frequency
					frequency_dict[k] += (self.given_frequency[k] * self.given_words_weight) / total_given_freq
		
		keys = frequency_dict.keys()
		vals = frequency_dict.values()
		i = 0
		while i < len(keys) - 1:
			if i >= 0 and vals[i] < vals[i+1]:
				keys[i], keys[i+1] = keys[i+1], keys[i]
				vals[i], vals[i+1] = vals[i+1], vals[i]
				i -= 1
			else:
				i += 1
		
		frequency = ''
		for c in keys:
			frequency += c

		return frequency
	
	# Find the index of the first vowel in letter frequency. This is used in solve_vc(). 
	# If the most common vowel is too rare, then it is likely that the executioner is 
	# choosing words that don't contain vowels. If that is so, then there is no point 
	# in selecting vowels before consonants.
	# 
	# For example, if the executioner is choosing the word 'q' every time, 'q' may 
	# quickly become the most common letter. But if solve_vc() is automatically choosing 
	# vowels before 'q', then it could run out of guesses before ever getting to 'q'.
	# But with this system it will guess 'a', then 'e', then 'i', but at that point there 
	# aren't any vowels left that are common enough. 'q' is chosen next, and the gueser 
	# wins.
	def find_first_vowel_index(self, frequency):
		first_vowel_index = 0
		i = 0
		for c in frequency:
			if WordList.re.search(self.vowel_match, c) != None:
				first_vowel = i
				break
			i += 1
		return first_vowel_index
	
	def find_given_words_weight(self):
		result = 0
		ratio = 0
		for arr in self.given_words_weights:
			if arr[1] / arr[2] > ratio:
				result = arr[0]
				ratio = arr[1] / arr[2]
		self.given_words_weight = result
		print "given words weights:", self.given_words_weights
		print "given words weight:", self.given_words_weight
		return result
	
	# Solve with vowels and consonants taken into account.
	def solve_vc(self, executioner):
		self.trials += 1
		
		# If this is enabled, given_words_weight will be selected out of the 
		# given_words_weights array. If it is disabled, given_words_weight will simply 
		# be the default.
		self.find_given_words_weight()

		frequency = self.modify_frequency()
		vowels = self.vowel_frequency
		consonants = self.consonant_frequency
		vowels_len = len(vowels); consonants_len = len(consonants)
		
		while executioner.is_playing:
			# If no vowels have been found yet, look for a vowel. Otherwise, choose 
			# randomly between a vowel and a consonant.
			new_vowels_len = len(WordList.re.findall(self.vowel_match, executioner.word))
			first_vowel_index = self.find_first_vowel_index(frequency)
			if len(vowels) > 0 and new_vowels_len == 0 and first_vowel_index < 10:
				letter = vowels[:1]
			else:
				letter = frequency[:1]
			
			print "guessing", letter
						
			if executioner.guess(letter) == True:
				for k in self.given_frequency:
					self.given_frequency[k] *= 1 - self.new_word_weight
					
				for c in executioner.word:
					self.given_frequency[c] += 1 * self.new_word_weight
				self.wins += 1
				break
			
			# The only possible words are words that don't contain letters known to be incorrect.
			finder = executioner.word.replace('.', '[' + executioner.not_incorrect + ']')
			
			frequency = self.modify_frequency(finder)
			
			for c in executioner.guessed:
				frequency = frequency.replace(c, '')
			
			vowels, consonants = self.vowel_consonant_frequency(frequency)
		
		i = -1
		for j in range(len(self.given_words_weights)):
			if self.given_words_weights[j][0] == self.given_words_weight:
				i = j
				break
		if executioner.did_guesser_win:
			self.given_words_weights[i][1] += 1
		else:
			self.given_words_weights[i][2] += 1
		
		for c in executioner.word:
			for k in self.given_frequency:
				self.given_frequency[k] *= 1 - self.new_word_weight
				
			for c in executioner.word:
				self.given_frequency[c] += 1 * self.new_word_weight
		return executioner.did_guesser_win
	
	
	# Solves Executioner by repeatedly re-evaluating the letter frequency in order to 
	# guess most effectively. This algorithm gets the correct result in 6 trials 
	# about 90% of the time.
	def solve_freq(self, executioner):
		self.trials += 1
		
		frequency = self.frequency
		while executioner.is_playing:
			letter = frequency[:1]
			if executioner.guess(letter) == True:
				self.wins += 1
				return True
			
			# The only possible words are words that don't contain letters known to be incorrect.
			finder = executioner.word.replace('.', '[' + executioner.not_incorrect + ']')
			
			frequency = wordlist.letter_frequency(wordlist.find_words(finder))
			for c in executioner.guessed:
				frequency = frequency.replace(c, '')
		return False
	
	
	# Solves Executioner by selecting the most common letters. Very dumb.
	def solve_quick(self, executioner):
		self.trials += 1
		frequency = self.frequency
		while executioner.is_playing:
			letter = frequency[:1]
			frequency = frequency[1:]
			if executioner.guess(letter) == True:
				self.wins += 1
				return True
		return False
	
	# Given an Executioner named executioner, try to guess what word the executioner 
	# chose. You can guess a letter with executioner.guess(letter). guess() will return 
	# True if the guesser wins, False if the guesser loses, and None if neither event 
	# occurs.
	def solve(self, executioner):
		return self.solve_vc(executioner)

	