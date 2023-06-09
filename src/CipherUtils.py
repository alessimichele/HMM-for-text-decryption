import random
import math


class CipherGenerator:
    def generate_cipher(self):
        """
        Generates a random cipher, which is a shuffled version of the alphabet.

        Returns:
            list: A list representing the generated cipher.
        """
        alphabet = list("abcdefghijklmnopqrstuvwxyz")
        random.shuffle(alphabet)
        return alphabet


class TextEncoder:
    def encode_text(self, text, cipher):
        """
        Encodes the given text using a cipher.

        Args:
            text (str): The input text to encode.
            cipher (list): The cipher to use for encoding.

        Returns:
            str: The encoded text.
        """
        encoded_text = []
        for char in text:
            if char.isalpha():
                index = ord(char.lower()) - ord("a")
                encoded_char = cipher[index]
                if char.isupper():
                    encoded_char = encoded_char.upper()
                encoded_text.append(encoded_char)
            else:
                encoded_text.append(char)
        return "".join(encoded_text)


class TextDecoder:
    def decode_text(self, text, cipher):
        """
        Decodes the given text using a cipher.

        Args:
            text (str): The input text to decode.
            cipher (list): The cipher to use for decoding.

        Returns:
            str: The decoded text.
        """
        decoded_text = []
        for char in text:
            if char.isalpha():
                index = cipher.index(char.lower())
                decoded_char = chr(index + ord("a"))
                if char.isupper():
                    decoded_char = decoded_char.upper()
                decoded_text.append(decoded_char)
            else:
                decoded_text.append(char)
        return "".join(decoded_text)


"""
class TextLik:
    def get_log_likelihood(self, text, probability_table):
        ""
        Calculates the log-likelihood of the given text based on a probability table.

        Args:
            text (str): The input text.
            probability_table (dict): A probability table mapping two-character sequences to their probabilities.

        Returns:
            float: The log-likelihood of the text.
        ""
        two_char_list = [text[i : i + 2] for i in range(len(text) - 1)]
        probabilities = [
            probability_table.get(two_char, 1 / len(probability_table))
            for two_char in two_char_list
        ]
        log_likelihood = sum(math.log(prob) for prob in probabilities)
        return log_likelihood
"""


class TextPreProcessor:
    def __init__(self, alphabet=list("abcdefghijklmnopqrstuvwxyz")):
        """
        Initializes the TextPreProcessor object with an alphabet.

        Args:
            alphabet (list, optional): The list of valid characters. Defaults to the lowercase alphabet.
        """
        self.alphabet = alphabet

    def has_uppercase(self, text):
        """
        Checks if the text contains uppercase characters.

        Args:
            text (str): The input text.

        Returns:
            bool: True if the text contains uppercase characters, False otherwise.
        """
        return any(char.isupper() for char in text)

    def lower(self, text):
        """
        Converts the text to lowercase.

        Args:
            text (str): The input text.

        Returns:
            str: The text converted to lowercase.
        """
        return text.lower()

    def unknown_chars(self, text):
        """
        Finds the unknown characters in the text that are not present in the alphabet.

        Args:
            text (str): The input text.

        Returns:
            list: A list of unknown characters found in the text.
        """
        if self.has_uppercase(text):
            raise ImportWarning(
                f"text={text} has upper case. Preprocess it using TextPreProcess class."
            )

        unknown_chars = []
        for char in text:
            if char not in self.alphabet and char not in unknown_chars:
                unknown_chars.append(char)
        return unknown_chars

    def remove_unknown_chars(self, text, unknown_chars):
        """
        Removes the unknown characters from the text.

        Args:
            text (str): The input text.
            unknown_chars (list): A list of unknown characters to be removed.

        Returns:
            str: The text with unknown characters removed.
        """
        for char in unknown_chars:
            text = text.replace(char, " ")
        return text

    def remove_additional_spaces(self, text):
        """
        Removes multiple whitespaces with only one if there are some.

        Args:
            text (str): The text to remove unknown characters from
        """
        text = " ".join(text.split())
        return text

    def save_text(self, text):
        """
        Saves the preprocessed text to a file named 'text_preprocessed.txt'.

        Args:
            text (str): The preprocessed text.
        """
        with open("outputs/text_preprocessed.txt", "w") as file:
            print(text, file=file)
