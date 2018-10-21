# TODO: Add skip_words list
from string import ascii_lowercase



skip_words = []

def normalise_input(input):
    lowercase_input = input.lower()

    words = []
    next_word = ""
    # Cycle through characters in the input, storing sequences of letters as words.
    for char in lowercase_input:
        if char in ascii_lowercase:
            next_word += char
        elif next_word != "":
            if next_word not in skip_words:
                words.append(next_word)
            next_word = ""
    
    # If a word was being read at the end of the string, add it to the list.
    if next_word != "":
        words.append(next_word)
    
    return words