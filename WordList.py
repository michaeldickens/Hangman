import random
import re

# A simpler version of the WordList program specially designed for Hangman.

class WordList:
		
	def __init__(self):
		self.wl_name = "wordlist.txt"
		myfile = open(self.wl_name, "r")
		self.lines = [ line.strip() for line in myfile.readlines() ]
	
	def add_word(self, word):
		for i in range(len(self.lines)):
			if word < self.lines[i]:
				self.lines.insert(i, word)
				break
		myfile = open(self.wl_name, "w")
		for line in self.lines:
			myfile.write(line + "\n")
	
	# 
	# Selects a random word out of the word list.
	# 
	# regex: Only select words that match this regular expression. If none is given, 
	# select any word with length greater than 0.
	# 
	def random(self, regex = '.+'):
		orig = index = random.randrange(len(self.lines))
		while True:
			if re.search(regex, self.lines[index]) != None:
				return self.lines[index]
			index += 1
			if index >= len(self.lines):
				index = 0
			if index == orig:
				return None
	
	
	# Takes a simplified regular expression and adds anchors to both ends. Thenn calls 
	# find_matches().
	def find_words(self, regex):
		if regex == None:
			return self.find_matches('.+')
		if not regex.startswith('^'):
			regex = '^' + regex
		if not regex.endswith('$'):
			regex += '$'
		return self.find_matches(regex)
	 
	# Returns a list of every word that matches regex.
	def find_matches(self, regex):
		return [line for line in self.lines if re.search(regex, line) != None]					
	
	
	def detailed_frequency(self, words = None):
		if words == None:
			words = self.lines	
		counts = [0 for i in range(0, 26)]
		letters = [chr(i+ord('a')) for i in range(0, 26)]
		
		# Add up all the letters.
		for word in words:
			for c in word:
				if ord(c) >= ord('a') and ord(c) <= ord('z'):
					counts[ord(c) - ord('a')] += 1
		
		# Sort the letters.
		i = 0
		while i < 25:
			if i >= 0 and counts[i] < counts[i+1]:
				letters[i], letters[i+1] = letters[i+1], letters[i]
				counts[i], counts[i+1] = counts[i+1], counts[i]
				i -= 1
			else:
				i += 1
		res = {}
		for i in range(0, len(letters)):
			res[letters[i]] = counts[i]
		return res
		
	# Calculates letter frequency based on the given list of words. If no list is given, 
	# instead uses the built-in list of words.
	def letter_frequency(self, words = None):
		if words == None:
			words = self.lines	
		counts = [0 for i in range(0, 26)]
		letters = [chr(i+ord('a')) for i in range(0, 26)]
		
		# Add up all the letters.
		for word in words:
			for c in word:
				if ord(c) >= ord('a') and ord(c) <= ord('z'):
					counts[ord(c) - ord('a')] += 1
		
		# Sort the letters.
		i = 0
		while i < 25:
			if i >= 0 and counts[i] < counts[i+1]:
				letters[i], letters[i+1] = letters[i+1], letters[i]
				counts[i], counts[i+1] = counts[i+1], counts[i]
				i -= 1
			else:
				i += 1
		
		freq = ''
		for letter in letters:
			freq += letter
		return freq

