from collections import Counter
from src.HMM_utils import string_to_numbers, map_alphabet_to_numbers
import numpy as np


class ProbabilityMatrix:
    def __init__(self, text):
        """
        Initializes the ProbabilityMatrix object with the provided text.

        Args:
            text (str): The input text.

        Raises:
            ImportWarning: If the text contains uppercase characters.
        """
        self.text = text
        self.all_2_chars = []
        self.probability_table = {}  # store the dictionary
        self.probability_matrix = None  # store the matrix
        self.normalized_matrix = (
            None  # store the normalized version of the matric, to be used in HMM
        )

        if self.has_uppercase():
            raise ImportWarning(
                f"text={text} has upper case. Preprocess it using TextPreProcess class."
            )

    def has_uppercase(self):
        """
        Checks if the text contains uppercase characters.

        Returns:
            bool: True if the text contains uppercase characters, False otherwise.
        """
        return any(char.isupper() for char in self.text)

    def break_into_two_chars(self, text):
        """
        Breaks the text into two-character sequences.

        Args:
            text (str): The input text.

        Returns:
            list: A list of two-character sequences.
        """
        return [text[i : i + 2] for i in range(len(text) - 1)]

    """def compute_probability_table(self):
        
        Computes the probability table for all two-character sequences in the text.
        The probability is calculated as the count of each sequence divided by the total count of all sequences.
        
        self.all_2_chars = self.break_into_two_chars(self.text)
        total_count = sum(Counter(self.all_2_chars).values())
        self.probability_table = {
            two_char: count / total_count
            for two_char, count in Counter(self.all_2_chars).items()
        }

        # check for missing bigrams in the corpus
        minimum = min(self.probability_table.values())
        print(minimum)
        for x in "abcdefghijklmnopqrstuvwxyz ":
            for y in "abcdefghijklmnopqrstuvwxyz ":
                if x + y not in self.probability_table:
                    self.probability_table[x + y] = minimum
                elif y + x not in self.probability_table:
                    self.probability_table[x + y] = minimum"""

    def compute_probability_table(self):
        """
        Computes the probability table for all two-character sequences in the text.
        The probability is calculated as the count of each sequence divided by the total count of all sequences.
        """
        # to not recompute all_2_chars, if there is (i.e. if it has been called already by compute_probability_matrix)
        if not self.all_2_chars:
            self.all_2_chars = self.break_into_two_chars(self.text)

        self.probability_table = {
            two_char: count / len(self.all_2_chars)
            for two_char, count in Counter(self.all_2_chars).items()
        }

        # check for missing bigrams in the corpus, add them to the dictionary
        minimum = min(self.probability_table.values())
        # print(minimum)
        for x in "abcdefghijklmnopqrstuvwxyz ":
            for y in "abcdefghijklmnopqrstuvwxyz ":
                if x + y not in self.probability_table:
                    self.probability_table[x + y] = minimum
                elif y + x not in self.probability_table:
                    self.probability_table[y + x] = minimum

        self.probability_table["  "] = 0

    def get_probability(self, two_char):
        """
        Retrieves the probability of a given two-character sequence. (using probability_table, the dict)

        Args:
            two_char (str): The two-character sequence.

        Returns:
            float: The probability of the given two-character sequence.
        """
        return self.probability_table[two_char]

    def compute_probability_matrix(self):
        # to not recompute all_2_chars, if there is (i.e. if it has been called already by compute_probability_table)
        if not self.all_2_chars:
            self.all_2_chars = self.break_into_two_chars(self.text)

        dict = Counter(self.all_2_chars).copy()
        for key in Counter(self.all_2_chars).keys():
            new_key = str(string_to_numbers(key, map_alphabet_to_numbers()))
            dict[new_key] = dict.pop(key)
        table = {
            two_char: count / len(self.all_2_chars) for two_char, count in dict.items()
        }

        probability_matrix = np.zeros((27, 27))

        for key in table.keys():
            i = eval(key)[0]
            j = eval(key)[1]
            probability_matrix[i, j] = table[key]

        self.probability_matrix = np.array(probability_matrix)

        minimum = np.min(self.probability_matrix[self.probability_matrix > 0])
        # print(minimum)

        self.probability_matrix = np.where(
            self.probability_matrix == 0, minimum, self.probability_matrix
        )

        self.probability_matrix[-1, -1] = 0

    def compute_normalized_matrix(self):
        if self.probability_matrix is None:
            self.compute_probability_matrix()
        row_sums = self.probability_matrix.sum(axis=1)

        # Normalize each row
        self.normalized_matrix = self.probability_matrix / row_sums[:, np.newaxis]

    def get_probability_mat(self, char_1, char_2):
        """
        Returns the probability of char_2 given char_1. (using probability_matrix, the matrix)

        Args:
        - char_1 (str): The preceding character.
        - char_2 (str): The following character.

        Returns:
        - float: The probability of char_2 given char_1.
        """
        alphabet = "abcdefghijklmnopqrstuvwxyz "
        idx_1 = alphabet.index(char_1)
        idx_2 = alphabet.index(char_2)
        return self.probability_matrix[idx_1, idx_2]

    def save_probability_table(self):
        """
        Saves the probability table to a file named 'probability_table.txt'.
        """
        with open("outputs/probability_table.txt", "w") as file:
            print(self.probability_table, file=file)

    def save_probability_matrix(self):
        """
        Saves the probability matrix to a file named 'probability_matrix.txt'.
        """
        with open("outputs/probability_matrix.txt", "w") as file:
            print(self.probability_matrix, file=file)

    def save_all_2_chars(self):
        """
        Saves the list of all two-character sequences to a file named 'all_2_chars.txt'.
        """
        with open("outputs/all_2_chars.txt", "w") as file:
            print(self.all_2_chars, file=file)
