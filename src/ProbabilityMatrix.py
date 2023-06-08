from collections import Counter


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
        self.probability_table = {}
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

    def compute_probability_table(self):
        """
        Computes the probability table for all two-character sequences in the text.
        The probability is calculated as the count of each sequence divided by the total count of all sequences.
        """
        self.all_2_chars = self.break_into_two_chars(self.text)
        total_count = sum(Counter(self.all_2_chars).values())
        self.probability_table = {
            two_char: count / total_count
            for two_char, count in Counter(self.all_2_chars).items()
        }

    def get_probability(self, two_char):
        """
        Retrieves the probability of a given two-character sequence.

        Args:
            two_char (str): The two-character sequence.

        Returns:
            float: The probability of the given two-character sequence.
        """
        prob_from_table = self.probability_table.get(two_char)
        if prob_from_table is None:
            return 1 / len(self.all_2_chars)
        else:
            return prob_from_table

    def save_probability_table(self):
        """
        Saves the probability table to a file named 'probability_table.txt'.
        """
        with open("outputs/probability_table.txt", "w") as file:
            print(self.probability_table, file=file)

    def save_all_2_chars(self):
        """
        Saves the list of all two-character sequences to a file named 'all_2_chars.txt'.
        """
        with open("outputs/all_2_chars.txt", "w") as file:
            print(self.all_2_chars, file=file)
