import random
import math
from src.CipherUtils import TextDecoder
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


class CipherBreaker:
    def __init__(self, starting_cipher, ciphered_text, probability_table):
        """
        Initializes the CipherBreaker object.

        Args:
            starting_cipher (list): The starting cipher to break.
            ciphered_text (str): The ciphered text.
            probability_table (dict): A probability table mapping two-character sequences to their probabilities.
        """
        self.current_cipher = starting_cipher
        self.ciphered_text = ciphered_text
        self.probability_table = probability_table

        self.decoder = (
            TextDecoder()
        )  # self.decoder.decode_text(text, permutated_cipher)

        self.history = {self.ciphered_text: [0, self.get_log_likelihood(self.ciphered_text)]}

        # self.decoded_texts = []  # List to store decoded texts

        # Store maximum log-likelihood achieved
        # self.max_log_lik = self.lik.get_log_likelihood(self.ciphered_text, probability_table)
        # self.max_lik_text = self.ciphered_text

    def swap(self, x):
        """
        Swaps two random elements in the list.

        Args:
            x (list): The list to perform the swap on.

        Returns:
            list: The list after the swap.
        """
        rand_indices = random.sample(range(len(x)), k=2)
        x[rand_indices[0]], x[rand_indices[1]] = x[rand_indices[1]], x[rand_indices[0]]
        return x

    def get_log_likelihood(self, text):
        """
        Calculates the log-likelihood of the given text based on a probability table.

        Args:
            text (str): The input text.

        Returns:
            float: The log-likelihood of the text.
        """
        two_char_list = [text[i : i + 2] for i in range(len(text) - 1)]
        probabilities = [
            self.probability_table.get(two_char, 1 / len(self.probability_table))
            for two_char in two_char_list
        ]
        log_likelihood = sum(math.log(prob) for prob in probabilities)
        return log_likelihood

    def break_cipher(self, iterations=10000, print_interval=20):
        """
        Breaks the cipher by performing iterations of swapping elements in the current cipher.

        Args:
            iterations (int, optional): The number of iterations to perform. Defaults to 10000.
            print_interval (int, optional): The interval at which to print the decoded text. Set to None to disable printing. Defaults to 20.

        Returns:
            list: The final deciphered cipher.
        """
        i = 0
        for _ in range(iterations):
            proposed_cipher = self.swap(self.current_cipher.copy())

            decoded_text_proposed = self.decoder.decode_text(
                self.ciphered_text, proposed_cipher
            )
            decoded_text_current = self.decoder.decode_text(
                self.ciphered_text, self.current_cipher
            )

            proposed_log_likelihood = self.get_log_likelihood(decoded_text_proposed)
            current_log_likelihood = self.get_log_likelihood(decoded_text_current)

            acceptance_probability = min(
                1, math.exp(proposed_log_likelihood - current_log_likelihood)
            )

            accept = random.choices(
                [True, False],
                weights=[acceptance_probability, 1 - acceptance_probability],
                k=1,
            )[0]

            if accept:
                self.current_cipher = proposed_cipher

                if print_interval is not None and i % print_interval == 0:
                    print(f"Iter {i}: {decoded_text_proposed}")
                i += 1

                # self.decoded_texts.append(decoded_text_proposed)  # Store decoded text
                self.history[decoded_text_proposed] = [ _ , proposed_log_likelihood]

        return self.current_cipher

    def extract_best(self, n_extract=5, return_likelihood=False):
        """
        Extracts the n_extract decoded texts with the highest log-likelihood.
        If log_lik = True it returns a list of item value pairs
        """
        sorted_dict = dict(
            sorted(self.history.items(), key=lambda x: x[1][1], reverse=True)
        )

        if return_likelihood == True:
            return list(sorted_dict.items())[:n_extract]

        return list(sorted_dict.keys())[:n_extract]

    def generate_animation(self, filename="cipher_iterations.gif"):
        """
        Generates an animation of the cipher breaking process and saves it as a GIF.
        """
        fig = plt.figure(figsize=(8, 6))  # Adjust the figure size as desired

        def update(i):
            plt.clf()
            # decoded_text = self.decoded_texts[i]
            decoded_text = list(self.history.keys())[i]
            lines = []
            current_line = ""
            for word in decoded_text.split():
                if (
                    len(current_line) + len(word) + 1 > 20
                ):  # Adjust the line length as desired
                    lines.append(current_line)
                    current_line = word
                else:
                    if current_line:
                        current_line += " "
                    current_line += word
            lines.append(current_line)

            justified_text = "\n".join(lines)
            plt.text(
                0.5, 0.5, justified_text, fontsize=16, ha="left", va="center"
            )  # Adjust the horizontal alignment to 'left'
            plt.axis("off")

        anim = FuncAnimation(
            fig, update, frames=len(self.history), interval=100
        )  # Decreased interval for faster animation

        if filename != "cipher_iterations.gif":
            filename = filename
        anim.save(f"GIF/{filename}", writer="imagemagick")
