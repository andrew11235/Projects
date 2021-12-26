from random import randrange
from english_words import english_words_lower_alpha_set as all_words  # Set of all alphabetic lowercase English words


# Tests if input is a single english letter
def test_char(c):
    try:
        if not 97 <= ord(c) <= 122:  # Unicode for lowercase letters a-z
            print('Please enter a lowercase English letter')
            return False

    except TypeError:
        print('You should input a single letter')
        return False

    return True


def main():
    print('Hangman : 8 tries to guess the word')  # Printing instructions
    words = list(all_words)  # Default set of all English words to guess from

    while True:
        setting = input('Type "play" to play the game, "custom" to use a custom word, "exit" to quit: ')

        if setting == 'play':
            # Initializing variables
            chosen_word = words[randrange(len(words))]
            word_set = set(chosen_word)
            guess_set = set()
            incorrect_list = []
            lives = 8

            # Plays game until win or loss
            while True:
                # Prints word with guessed letters and blanks
                print('\n' + ''.join(let if let in guess_set else '-' for _, let in enumerate(chosen_word)))

                guess = input('\nInput a letter: ')

                # Tests if input is a single english letter
                if not test_char(guess):
                    pass
                # Tests if input has already been entered before
                elif guess in guess_set:
                    print("You've already guessed this letter\n")
                # Otherwise, tests if input is in the word and subtracts a life if not
                elif guess not in word_set:
                    print("That letter doesn't appear in the word\n")
                    incorrect_list.append(guess)
                    lives -= 1

                guess_set.add(guess)

                # Test for win and loss
                if word_set.issubset(guess_set):
                    print('\nYou guessed the word!\n')
                    break
                elif lives == 0:
                    print(f'You lost! The word was: {chosen_word}\n')
                    break

                # Prints the incorrect guesses and
                print('\n' + '=' * 45)
                print('Incorrect guesses: ' + ', '.join(let for let in incorrect_list))
                print(f'Lives left: {lives}')

        # User input for a custom word
        elif setting == 'custom':
            words = [input('Enter custom word: ').lower()]
            print('\n' * 99)  # Prints newlines to hide input custom word

        elif setting == 'exit':
            exit()

        else:
            print()
            pass


if __name__ == '__main__':
    main()
