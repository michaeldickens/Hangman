'''
This is the actual executioner that gets run.
'''


import WordList
import random
import math

wordlist = WordList.WordList()

class Executioner:
	
	# Initialize an Executioner, ready to play. Please do not change anything already 
	# in this method, but feel free to add more stuff.
	def __init__(self):
		self.iterator = 0
		
		self.alltime_hardest_words = dict([(line.split()[0], int(line.split()[1])) for line in open("alltime_hardest_words.txt", "r") ])
		
		self.random_games = 0
		self.max_random_games = 30
		self.win_count = 0
		self.lose_count = 0.001 # Avoid division by zero.
		self.new_win_or_loss_weight = 1.0 / 20
		self.average_ratio = 0
		self.tries_below_average = 0
		self.tries_before_change = 10
		self.choose_word_count = 2048
		self.choose_word_counts = [ [16**i, 5, 5.0] for i in range(1, 4) ]
		self.select_count_each = 0
		self.select_count_each_max = 32
				
		self.did_guesser_win = False
		self.reset()
	
	# Chooses a word for the Guesser to guess. Your Executioner should choose a word 
	# that's going to be as hard to guess as possible.
	def choose_word(self):
		frequency = wordlist.letter_frequency()
		count = self.choose_word_count
		
		if count > len(wordlist.lines):
			count = len(wordlist.lines) - 1
		start = random.randrange(len(wordlist.lines) - count)
		best_word = ''
		best_score = 0
		for i in range(start, start + count):
			score = self.score_word(frequency, wordlist.lines[i])
			if score > best_score:
				best_word = wordlist.lines[i]
				best_score = score
		self.iterator += 1
				
		# These four make the combination of words that is the hardest to get.
#		return ["buzz", "pyx", "miff", "vow"][self.iterator % 4]
		return best_word
	
	# Scores a word based on how rare the letters in it are.
	def score_word(self, frequency, word):
		score = 0.0
		for letter in word:
			if letter in frequency:
				score += frequency.index(letter)
		score /= len(word)**1.5
		if len(word) <= 2:
			score /= (4 - len(word))**2
		
		if word in self.alltime_hardest_words and self.alltime_hardest_words[word] > 0:
			score += math.log(self.alltime_hardest_words[word], 2)
		
		return score

	# Print out every possible word for the given count.
	def all_words_for_count(self, count=None):
		frequency = wordlist.letter_frequency()
		if count == None:
			count = len(wordlist.lines)
		scores = []
		for i in range(0, count):
			score = self.score_word(frequency, wordlist.lines[i])
			scores.append([wordlist.lines[i], score])
		scores.sort(lambda x, y: cmp(x[1], y[1]))
		for score in scores:
			print score[0], 'scores', score[1]
			
	
	# Uses RVS 2
	def find_best_count(self):
		i = int(math.log(self.choose_word_count, 16)) - 1
		if self.did_guesser_win:
			self.choose_word_counts[i][2] += 1
		else:
			self.choose_word_counts[i][1] += 1

		if self.select_count_each < self.select_count_each_max:
			i = self.select_count_each % 3
			self.choose_word_count = self.choose_word_counts[i][0]
			print "calculating", self.choose_word_count
			self.select_count_each += 1
		else:
			best = 0
			ratio = 0
			for arr in self.choose_word_counts:
				if arr[1] / arr[2] > ratio:
					best = arr[0]
					ratio = arr[1] / arr[2]
			print self.choose_word_counts
			print "count =", best, "(" + str(ratio) + ")"
			self.choose_word_count = best
			return self.choose_word_count
	
	# For the first (self.max_random_games) games, generate (self.choose_word_count) 
	# randomly and find the average ratio. Then randomly select (self.choose_word_count) 
	# and change it if the current ratio ever falls below the average for too long.
	# Uses RVS 3
	def track_count(self):
		if self.did_guesser_win:
			self.lose_count *= 1 - self.new_win_or_loss_weight
			self.lose_count += 1 * self.new_win_or_loss_weight
		else:
			self.win_count *= 1 - self.new_win_or_loss_weight
			self.win_count += 1 * self.new_win_or_loss_weight
		
		if self.random_games < self.max_random_games:
			self.random_games += 1
			self.choose_word_count = 2**(random.randrange(15)) # max is 16384
		elif self.random_games == self.max_random_games:
			# The executioner is done finding the average ratio.
			self.random_games += 1
			self.average_ratio = float(self.win_count) / self.lose_count
			print self.win_count, "wins,", self.lose_count, "losses"
			print "average ratio:", self.average_ratio
			self.win_count = 0
			self.lose_count = 0.001
		elif float(self.win_count) / self.lose_count < self.average_ratio: 
			self.tries_below_average += 1
		
		if self.tries_below_average > self.tries_before_change:
			# If the ratio is worse than average, change self.choose_word_count.
			self.tries_below_average = 0
			print "count", self.choose_word_count, "has fallen to", (float(self.win_count) / self.lose_count), 
			self.choose_word_count = 2**(random.randrange(15))
			print "changing count to", self.choose_word_count
			self.win_count = 0
			self.lose_count = 0.001
		
	
	# Reset the Executioner before each new game.
	def reset(self, word=None):
#		self.track_count()
#		self.find_best_count()
		
		if word == None:
			self._word = self.choose_word()
		else:
			self._word = word
		# ...
		self.length = len(self._word)
		self.word = '.' * self.length
		self.man = 0 # How many parts have been drawn on the man.
		self.body_parts = 6 # The guesser loses when he gets this many body parts.
		self.guessed = '' # Contains all guesses, whether correct or not.
		self.not_incorrect = 'abcdefghijklmnopqrstuvwxyz' # Contains all letters that were not incorrect guesses.
		self.is_playing = True
		self.did_guesser_win = False
	
	def add_to_hardest_words(self, word, count):
		if word in self.alltime_hardest_words:
			self.alltime_hardest_words[word] += count
		else:
			self.alltime_hardest_words[word] = count
	
	
	# 
	# A return value of True indicates a win, False indicates a loss. None indicates 
	# that neither event occurred.
	# 
	# Please do not modify this method.
	# 
	def guess(self, letter):
		if self.is_playing == False:
			return self.did_guesser_win
		
		if letter in self.guessed:
			print "You already guessed '" + str(letter) + "'!"
			return None

		self.guessed += letter

		if letter in self._word:
			wlist = list(self._word)
			nlist = list(self.word)
			self.word = ''
			for i in range(0, self.length):
				if wlist[i] == letter:
					nlist[i] = letter
				self.word += nlist[i]


			if not '.' in self.word:
				self.is_playing = False
				self.did_guesser_win = True
				print "The guesser wins! The word is", self._word
				self.add_to_hardest_words(self._word, -1)
				self.word = self._word
				return True
		else:
			self.not_incorrect = self.not_incorrect.replace(letter, '')
			self.man += 1
			if self.man >= self.body_parts:
				self.is_playing = False
				self.did_guesser_win = False
				print "The guesser loses! It had " + self.word + ", the word was " + self._word + "."
				self.add_to_hardest_words(self._word, 1)
				self.word = self._word
				return False
		return None
	
	def end_game(self):
		myfile = open("alltime_hardest_words.txt", "w")
		for k, v in self.alltime_hardest_words.iteritems():
			if v > 0:
				myfile.write(k + " " + str(v) + "\n")
		