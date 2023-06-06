import numpy as np


class ProbabilityMatrix:
    """
    A class for computing and working with a probability matrix based on a given text and alphabet.

    Attributes:
    - text (str): The input text used to compute the probability matrix.
    - alphabet (str): The characters that make up the alphabet.
    - matrix (numpy.ndarray): The probability matrix computed from the text.

    Methods:
    - __init__(text, alphabet): Initializes a ProbabilityMatrix instance.
    - compute_matrix(): Computes the probability matrix based on the input text.
    - get_probability(char_1, char_2): Returns the probability of char_2 given char_1.
    - print_probabilities(): Prints the probabilities of all character pairs in the alphabet.
    - unknown_chars(): Finds the unknown characters in the text that are not in the alphabet.
    - preprocess_text(unknown_chars): Removes the unknown characters from the text.
    - print_transition_probabilities(): Prints the transition probabilities from the most likely down to 0.
    """

    def __init__(self, text, alphabet):
        """
        Initializes a ProbabilityMatrix instance.

        Args:
        - text (str): The input text used to compute the probability matrix.
        - alphabet (str): The characters that make up the alphabet.
        """
        self.text = text
        self.alphabet = alphabet
        self.matrix = np.zeros((len(alphabet), len(alphabet)))

        if " " not in self.alphabet:
            raise Warning("No space character " " in the alphabet.")

        # Swap space character with the last character in the alphabet, if necessary
        if " " in self.alphabet and self.alphabet[-1] != " ":
            idx_space = self.alphabet.index(" ")
            self.alphabet[idx_space], self.alphabet[-1] = (
                self.alphabet[-1],
                self.alphabet[idx_space],
            )

    def compute_matrix(self):
        """
        Computes the probability matrix based on the input text.
        """
        for i in range(len(self.text) - 1):
            current_char = self.text[i]
            next_char = self.text[i + 1]

            if current_char in self.alphabet and next_char in self.alphabet:
                current_index = self.alphabet.index(current_char)
                next_index = self.alphabet.index(next_char)
                self.matrix[next_index, current_index] += 1

            elif current_char not in self.alphabet:
                raise ValueError(f"Character: {current_char} not in alphabet")

            elif next_char not in self.alphabet:
                raise ValueError(f"Character: {next_char} not in alphabet")

        if " " in self.alphabet:
            idx_space = self.alphabet.index(" ")
            self.matrix = np.delete(
                np.delete(self.matrix, idx_space, axis=0), idx_space, axis=1
            )
        ones = np.sum(self.matrix)
        self.matrix = self.matrix / ones

    def compute_matrix_spaces(self):
        """
        Computes the probability matrix based on the input text.
        It also preserves the white spaces in this case
        """
        for i in range(len(self.text) - 1):
            current_char = self.text[i]
            next_char = self.text[i + 1]

            if current_char in self.alphabet and next_char in self.alphabet:
                current_index = self.alphabet.index(current_char)
                next_index = self.alphabet.index(next_char)
                self.matrix[next_index, current_index] += 1

            elif current_char not in self.alphabet:
                raise ValueError(f"Character: {current_char} not in alphabet")

            elif next_char not in self.alphabet:
                raise ValueError(f"Character: {next_char} not in alphabet")

        ones = np.sum(self.matrix)
        self.matrix = self.matrix / ones

    def compute_log_matrix(self):
        """
        Compute matrix storing log transition probabilities
        I adjust to avoid taking the log of 0 by adding 1
        """
        log_matrix = np.zeros_like(self.matrix)
        return np.log(self.matrix + 1)

    def get_probability(self, char_1, char_2):
        """
        Returns the probability of char_2 given char_1.

        Args:
        - char_1 (str): The preceding character.
        - char_2 (str): The following character.

        Returns:
        - float: The probability of char_2 given char_1.
        """
        idx_1 = self.alphabet.index(char_1)
        idx_2 = self.alphabet.index(char_2)
        return self.matrix[idx_1][idx_2]

    def print_probabilities(self):
        """
        Prints the probabilities of all character pairs in the alphabet.
        """
        for x in self.alphabet[:-1]:
            for y in self.alphabet[:-1]:
                x_idx = self.alphabet.index(x)
                y_idx = self.alphabet.index(y)
                print(f"p({x}|{y}) = {self.matrix[x_idx][y_idx]}")

    def print_transition_probabilities(self):
        """
        Prints the transition probabilities from the most likely down to 0.
        """
        sorted_probs = sorted(self.matrix.flatten(), reverse=True)
        for prob in sorted_probs:
            if prob == 0:
                break
            x_idx, y_idx = np.where(self.matrix == prob)
            x_char = self.alphabet[x_idx[0]]
            y_char = self.alphabet[y_idx[0]]
            print(f"p({y_char}|{x_char}) = {prob}")

    def unknown_chars(self):
        """
        Finds the unknown characters in the text that are not in the alphabet.

        Returns:
        - list: A list of unknown characters.
        """
        self.text = " ".join(self.text.split())
        self.text = self.text.lower()

        unknown_chars = []
        for char in self.text:
            if char not in self.alphabet and char not in unknown_chars:
                unknown_chars.append(char)
        return unknown_chars

    def preprocess_text(self, unknown_chars):
        """
        Removes the unknown characters from the text.

        Args:
        - unknown_chars (list): A list of unknown characters.
        """
        for char in unknown_chars:
            self.text = self.text.replace(char, " ")
