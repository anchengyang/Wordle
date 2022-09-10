import random
import os
import math

def generate_random_guess_word(possible_words):
    return random.choice(possible_words)

def calc_letter_entropy(freq):
    p = freq
    return -1 * p * math.log2(p) - (1-p) * math.log2(1-p)

def calc_word_entropy(word, freq_dict):
    total = 0
    for l in word:
        freq = freq_dict[l]
        total += calc_letter_entropy(freq)
    return total

def freq_words(possible_words):
    freq_dict = {'e':0.111607, 't':0.069509, 'a':0.084966, 'o':0.071635, 'i':0.075448, 'n':0.066544, 's':0.057351, 'r':0.075809, 'l':0.054893, 'c':0.045388, 'u': 0.036308, 'd':0.033844, 'p':0.031671, 'm': 0.030129, 'h':0.030034, 'g':0.024705, 'b':0.020720, 'f':0.018121, 'y':0.017779, 'w':0.012899, 'k': 0.011016, 'v':0.010074, 'x':0.002902, 'z':0.002722, 'j':0.001965, 'q':0.001962}
    
    max_entropy = float('-inf')
    max_entropy_word = ''
    for word in possible_words:
        entropy = calc_word_entropy(word, freq_dict)
        if entropy > max_entropy:
            max_entropy = entropy
            max_entropy_word = word
    
    return max_entropy_word

#should calc entropy for all possible_words then pick the highest
def generate_smart_guess(word_list, possible_words, nth_guess):
    return freq_words(possible_words)

def filter_available_words(guess_word, colours, possible_words):
    
    def check(word):
        result = True
        if len(word) != len(guess_word):
            return False
        else:
            lst_word = list(word)
            lst_guess = list(guess_word)
            
            # settle all the G first
            for i in range(len(lst_word)):
                letter = lst_guess[i]
                if colours[i] == "G":
                    if letter == lst_word[i]:
                        result = result and True
                        # * represents the letter that has been seen and meets the condition
                        lst_word[i] = '*'
                        lst_guess[i] = '*'
                    else:
                        return False
            
            #settling Y and B    
            # check if the letter in the guess word is equal to the letter in the possible word at all indices
            for i in range(len(lst_word)):
                if lst_word[i] != '*' and lst_word[i] == lst_guess[i]:
                        return False
            
            for i in range(len(lst_word)):
                guess_letter = lst_guess[i]
                # skip the iteration if the letter is an *
                if guess_letter == '*':
                    continue
                # if result is false then return
                if result == False:
                    return False
                
                #count number of Y and B of the current letter
                num_of_Y = 0
                num_of_B = 0
                for j in range(len(lst_word)):
                    if colours[j] == "Y" and guess_letter == lst_guess[j]:
                        num_of_Y += 1
                    elif colours[j] == "B" and guess_letter == lst_guess[j]:
                        num_of_B += 1
                
                # if number of B is 0, means the possible word can have 
                # occurences of the letter more than or equal to the number of Y
                if num_of_B == 0 and num_of_Y > 0:
                    if lst_word.count(guess_letter) >= num_of_Y:
                        result = result and True
                    else:
                        return False
                # if number of Y is 0, means the possible word must have
                # 0 occurences of the letter
                elif num_of_B > 0 and num_of_Y == 0:
                    if lst_word.count(guess_letter) == 0:
                        result = result and True
                    else:
                        return False
                # if number of B and Y is more than 0, means the possible word must have 
                # occurences of the letter equal to the number of Y
                else:
                    if lst_word.count(guess_letter) == num_of_Y:
                        result = result and True
                    else:
                        return False
                    
                # set all occurences of the letter in both words to be *
                for index in range(len(lst_word)):
                    if lst_word[index] == guess_letter:
                        lst_word[index] = '*'
                    if lst_guess[index] == guess_letter:
                        lst_guess[index] = '*'
                    
            return result
    
    return list(filter(check, possible_words))

def make_evaluate_guess(word, word_list):
    def evaluate_guess(guess_word):
        if guess_word not in word_list:
            raise Exception("Guess word not in word list")
        word_length = len(word)
        if len(guess_word) != word_length:
            raise Exception("Guess word not of correct length")

        result = ['B']*word_length
        word_l = list(word)
        ignore_index = []
        for i in range(word_length):
            if i in ignore_index:
                continue
            if guess_word[i] == word_l[i]:
                result[i] = 'G'
                word_l[i] = '-'
                ignore_index.append(i)
        for i in range(word_length):
            if i in ignore_index:
                continue
            for j in range(word_length):
                if guess_word[i] == word_l[j]:
                    result[i] = 'Y'
                    word_l[j] = '-'
                    break
        return ''.join(result)
    return evaluate_guess

def solver(word_list, evaluate_guess_func):
    count = 1
    possible_words = word_list
    while len(possible_words) != 1 and count <= 6:
        guess_word = generate_smart_guess(word_list, possible_words, count)
        colours = evaluate_guess_func(guess_word)
        new_word_list = filter_available_words(guess_word, colours, possible_words)
        possible_words = new_word_list
        count+=1
    if len(possible_words) == 1:
        print(count)
        return possible_words[0]
    else:
        print('EXCEED 6')
        return possible_words


if __name__ == "__main__":
    # Load word list from words.txt 
    # Put the words.txt in the same directory as ps2.ipynb
    dir_path = os.getcwd()
    word_list = open(os.path.join(dir_path, 'words.txt'), 'r').read().splitlines()

    ''' Test cases for `solver` '''
    tests_game = make_evaluate_guess("tests", word_list)
    print(solver(word_list, tests_game)) # Should print 'tests'

    cases_game = make_evaluate_guess("cases", word_list)
    print(solver(word_list, cases_game)) # Should print 'cases'

    which_game = make_evaluate_guess("which", word_list)
    print(solver(word_list, which_game)) # Should print 'which'