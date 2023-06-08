import random
import math
from src.CipherUtils import TextDecoder, TextLik
import multiprocessing

"""
Class not used in any code
    - implements a double swap (swap two letters instead of one)
    - implements a in-parallel step inside break_cipher:
        - two swap are done in parallel and then the best one is chosen
"""


class CipherBreaker:
    def __init__(self, starting_cipher, ciphered_text, probability_table):
        self.current_cipher = starting_cipher
        self.ciphered_text = ciphered_text
        self.probability_table = probability_table

        self.decoder = TextDecoder()  # self.decoder.decode_text
        self.lik = TextLik()  # self.lik.get_log_lik_text

        self.decoded_texts = []  # List to store decoded text

    def parallel_swap(self, x):
        rand_indices = random.sample(range(len(x)), k=2)
        x[rand_indices[0]], x[rand_indices[1]] = x[rand_indices[1]], x[rand_indices[0]]
        return x

    def evaluate_swap(self, swap):
        proposed_cipher = swap(self.current_cipher.copy())

        decoded_text_proposed = self.decoder.decode_text(
            self.ciphered_text, proposed_cipher
        )
        proposed_log_likelihood = self.lik.get_log_lik_text(
            decoded_text_proposed, self.probability_table
        )

        return proposed_cipher, decoded_text_proposed, proposed_log_likelihood

    def break_cipher(self, iterations=10000, print_interval=20):
        i = 0
        for _ in range(iterations):
            swap_pool = multiprocessing.Pool()
            swaps = [self.parallel_swap] * multiprocessing.cpu_count()
            results = swap_pool.map(self.evaluate_swap, swaps)
            swap_pool.close()
            swap_pool.join()

            best_swap = max(results, key=lambda x: x[2])
            proposed_cipher, decoded_text_proposed, proposed_log_likelihood = best_swap

            decoded_text_current = self.decoder.decode_text(
                self.ciphered_text, self.current_cipher
            )
            current_log_likelihood = self.lik.get_log_lik_text(
                decoded_text_current, self.probability_table
            )

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

                self.decoded_texts.append(decoded_text_proposed)  # Store decoded text
