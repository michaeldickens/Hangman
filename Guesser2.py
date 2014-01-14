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
			if total_letter_freq != 0:
				frequency_dict[k] = (letters[k] * (1 - self.given_words_weight)) / total_letter_freq
			
		for k in self.given_frequency:
			if total_given_freq != 0:
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
	
	# Solve with vowels and consonants taken into account.
	def solve_vc(self, executioner):
		self.trials += 1
		
		frequency = self.modify_frequency()
		vowels = self.vowel_frequency
		consonants = self.consonant_frequency
		vowels_len = len(vowels); consonants_len = len(consonants)
		
		while executioner.is_playing:
			# If no vowels have been found yet, look for a vowel. Otherwise, choose 
			# randomly between a vowel and a consonant.
			new_vowels_len = len(WordList.re.findall(self.vowel_match, executioner.word))
			if len(vowels) > 0 and new_vowels_len == 0:
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
				return True
			
			# The only possible words are words that don't contain letters known to be incorrect.
			finder = executioner.word.replace('.', '[' + executioner.not_incorrect + ']')
			
			frequency = self.modify_frequency(finder)
			
			for c in executioner.guessed:
				frequency = frequency.replace(c, '')
			
			vowels, consonants = self.vowel_consonant_frequency(frequency)
		
		for c in executioner.word:
			for k in self.given_frequency:
				self.given_frequency[k] *= 1 - self.new_word_weight
				
			for c in executioner.word:
				self.given_frequency[c] += 1 * self.new_word_weight
		return False
	
	
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

