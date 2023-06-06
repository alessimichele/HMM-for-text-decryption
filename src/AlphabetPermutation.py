import random
from datetime import datetime


class AlphabetPermutation:
    """
    A class for generating and working with an alphabet permutation.

    Attributes:
    - alphabet (list): The list of characters representing the alphabet.
    - permutation (dict): The generated permutation mapping.

    Methods:
    - __init__(alphabet): Initializes an AlphabetPermutation instance.
    - generate_permutation(): Generates a random permutation of the alphabet.
    - describe_permutation(): Prints and returns the generated permutation.
    - permute_string(string): Permutes a given string based on the generated permutation.
    """

    def __init__(self, alphabet):
        """
        Initializes an AlphabetPermutation instance.

        Args:
        - alphabet (list): The list of characters representing the alphabet.
        """
        self.alphabet = alphabet
        self.permutation = self.generate_permutation()

    def generate_permutation(self):
        """
        Generates a random permutation of the alphabet.

        Returns:
        - dict: The generated permutation mapping.
        """
        random.seed(datetime.now().timestamp())
        alphabet_list = self.alphabet.copy()
        alphabet_list.remove(" ")
        random.shuffle(alphabet_list)
        permutation = {
            self.alphabet[i]: alphabet_list[i] for i in range(len(alphabet_list))
        }
        return permutation

    def describe_permutation(self):
        """
        Prints and returns the generated permutation.

        Returns:
        - dict: The generated permutation mapping.
        """
        print("Permutation:")
        for char in self.permutation:
            print(char, "->", self.permutation[char])
        return self.permutation

    def permute_string(self, string):
        """
        Permutes a given string based on the generated permutation.

        Args:
        - string (str): The string to be permuted.

        Returns:
        - str: The permuted string.
        """
        string = string.lower()
        permuted_string = ""
        for char in string:
            if char in self.permutation:
                permuted_string += self.permutation[char]
            else:
                permuted_string += char
        return permuted_string


    def swap_letters(self, i, j):
        """
        Given the position of two letters to swap (so if we give 0, 1 it will swap the values associated to a and b)
        """
        if (i < 0 | i > 25 | j < 0 | i > 25):
            print("You are messing things up you can't call it on these")
        i = chr(i + 97)
        j = chr(j + 97)

        self.permutation[i], self.permutation[j] = self.permutation[j], self.permutation[i] 
        
