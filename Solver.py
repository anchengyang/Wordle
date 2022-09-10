import random
import os
import math

def generate_random_guess_word(possible_words):
    return random.choice(possible_words)


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
    if len(word_list) == 1:
        return word_list[0]
    elif word_list == []:
        return "NOT POSSIBLE"
    else:
        guess_word = generate_random_guess_word(word_list)
        colours = evaluate_guess_func(guess_word)
        new_word_list = filter_available_words(guess_word, colours, word_list)
        return solver(new_word_list, evaluate_guess_func)



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