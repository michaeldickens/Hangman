import Guesser
import Executioner
import WordList

def end_game(guesser, executioner):
	executioner.end_game()

def play():
	guesser = Guesser.Guesser()
	executioner = Executioner.Executioner()
	guesser.solve(executioner)
	return executioner.did_guesser_win

def repeat(trials):
	guesser_wins = 0
	guesser = Guesser.Guesser()
	executioner = Executioner.Executioner()
	for i in range(1, trials):
		guesser.solve(executioner)
		if executioner.did_guesser_win:
			guesser_wins += 1
		executioner.reset()
	print 'Out of', trials, 'trials, the guesser won', guesser_wins, \
	'times and the executioner won', trials - guesser_wins, 'times.'

def repeat2(trials):
	guesser_wins = 0
	guesser = Guesser.Guesser()
	executioner = Executioner.Executioner()
	highest_to_guess = 0
	for i in range(1, trials):
		guesser.solve(executioner)
		if executioner.did_guesser_win:
			guesser_wins += 1
		if executioner.man + len(executioner.word) > highest_to_guess:
			highest_to_guess = executioner.man + len(executioner.word)
		print 'highest to guess: ' + str(highest_to_guess)
		executioner.reset()
	print 'Out of', trials, 'trials, the highest number of guesses was ' + str(highest_to_guess)


def play_hangman_executioner():	
	# This is rather primitive, and people might not trust the program.

	guesser = Guesser.Guesser()
	executioner = Executioner.Executioner()
	wins = 0
	losses = 0
	while True:
		word = raw_input('What is your word? ').strip()
		if (word == '-q'):
			end_game(guesser, executioner)
			return None
		
		while len(Guesser.wordlist.find_words(word)) == 0:
			word = raw_input('That is not a word. What is your word? ').strip()			
		executioner.reset(word)
		guesser.solve(executioner)
		if executioner.did_guesser_win:
			losses += 1
		else:
			wins += 1
		print 'You have', wins, 'wins and', losses, 'losses'
		print

def play_hangman_guesser():
	executioner = Executioner.Executioner()
	while True:
		executioner.reset()
		incorrect = ''
		while executioner.is_playing:
			print "word:", executioner.word
			print "guessed letters:", incorrect
			print "body parts remaining:", executioner.body_parts - executioner.man
			while True:
				letter = raw_input('What is your guess? ').strip()
				if (letter == '-q'):
					end_game(guesser, executioner)
					return None

				if len(letter) > 1:
					print "That is more than just one letter. Please try again."
				elif ord(letter) < ord('a') or ord(letter) > ord('z'):
					print "You must enter a lowercase letter. Please try again."
				else:
					break
			if executioner.guess(letter) != None:
				break
			if not letter in executioner.not_incorrect and not letter in incorrect:
				incorrect += letter
			print

def play_hangman_both():
	guesser = Guesser.Guesser()
	executioner = Executioner.Executioner()
	wins = 0
	losses = 0
	myfile = open('results.txt', 'a')
	while True:
		word = raw_input('What is your word? ').strip()
		if (word == '-q'):
			end_game(guesser, executioner)
			return None
		
		while len(Guesser.wordlist.find_words(word)) == 0:
			addp = raw_input('That is not a word. ' + 
					'Do you want to add it to the dictionary? (y/n) ').strip()
			if addp == 'y':
				print 'Adding...'
				Guesser.wordlist.add_word(word)
				Guesser.wordlist = WordList.WordList()
				Executioner.wordlist = WordList.WordList()
				print 'added.'
			word = raw_input('What is your word? ').strip()
			if (word == '-q'):
				end_game(guesser, executioner)
				return None
		executioner.reset(word)
		guesser.solve(executioner)
		if executioner.did_guesser_win:
			losses += 1
			myfile.write("Computer | " + (executioner._word + ' ' * (14 - len(executioner._word))) + " | computer\n")
		else:
			myfile.write("Computer | " + (executioner._word + ' ' * (14 - len(executioner._word))) + " | human\n")
			wins += 1
		print 'You have', wins, 'wins and', losses, 'losses'
		print
		
		executioner.reset()
		incorrect = ''
		while executioner.is_playing:
			print "word:", executioner.word
			print "guessed letters:", incorrect
			print "body parts remaining:", executioner.body_parts - executioner.man
			while True:
				letter = raw_input('What is your guess? ').strip()
				if (letter == '-q'):
					end_game(guesser, executioner)
					return None
				if len(letter) > 1:
					print "That is more than just one letter. Please try again."
				elif len(letter) == 0:
					print "You didn't enter anything. Please try again."
				elif ord(letter) < ord('a') or ord(letter) > ord('z'):
					print "You must enter a lowercase letter. Please try again."
				else:
					break
			if executioner.guess(letter) != None:
				break
			if not letter in executioner.not_incorrect and not letter in incorrect:
				incorrect += letter
			print
		if executioner.did_guesser_win:
			wins += 1
			myfile.write("Human    | " + (executioner._word + ' ' * (14 - len(executioner._word))) + " | human\n")
		else:
			myfile.write("Human    | " + (executioner._word + ' ' * (14 - len(executioner._word))) + " | computer\n")
			losses += 1
		print 'You have', wins, 'wins and', losses, 'losses'
		print
	myfile.close()
	

#repeat2(1000)
#play_hangman_executioner()
#play_hangman_guesser()
play_hangman_both()
#ex = Executioner.Executioner()
#ex.all_words_for_count()

