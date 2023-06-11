from difflib import SequenceMatcher
import matplotlib.pyplot as plt
import numpy as np

from src.CipherBreaker import CipherBreaker
from src.CipherUtils import (
    TextDecoder,
    TextEncoder,
    CipherGenerator,
    TextPreProcessor,
)
from src.ProbabilityMatrix import ProbabilityMatrix

from difflib import SequenceMatcher


def similar(a, b):
    """
    Given two strings a, b it returns a percentage of matching characters among the two
    """

    return SequenceMatcher(None, a.replace(" ", ""), b.replace(" ", "")).ratio()


def prepare_subtexts(path_to_file, lengths):
    """
    This function returns the subtext to use to assess accuracy in decryption

    Input:
        - path_to_file (str) giving the path to the text file
        - lengths (list of int) giving the text lengths to consider
    """
    preprocess = TextPreProcessor()
    with open(path_to_file, "r") as input_file:
        full_text = input_file.read()

    full_text = preprocess.lower(full_text)
    unknown_chars = preprocess.unknown_chars(full_text)
    full_text = preprocess.remove_unknown_chars(full_text, unknown_chars=unknown_chars)
    full_text = preprocess.remove_additional_spaces(full_text)

    subtexts = [
        " ".join(full_text.split()[: lengths[i]]) for i in range(len(lengths))
    ]  # Contains the ones for the varying lengths

    return subtexts


def accuracy_varying_text_length(
    subtexts,
    cipher_generator,
    probability_matrix,
    extract_top=5,
    n_iterations=3,
    max_iterations=10000,
    nstart=3,
):
    """
    This function assesses the accuracy of the MCMC decryption.
    Input:
        - subtexts (list of str): a vector of text of different length
        - cipher_generator (CipherGenerator instance)
        - probability_matrix
        - extract_top(int) : After cipher breaking how many of the top ones we want to retain
        - n_iterations (int) : number of times we want to repeat the encryption-decryption for each text
        - max_iterations (int) : number of iterations in the cipher breaking procedure
        - nstart (int) : number of starting points in the cipher breaking procedure

    For each subtext it encrypts it and decrypts it n_iteration times.
        Everytime it finishes decrypting it compares the best extract_top (in terms of log likelihood) with the original string,
        and computes the accuracy as the proportion of characters matching for the string which matches best.
        Then for each subtext these are averaged over all n_iterations runs and are stored.
    """
    text_encoder = TextEncoder()
    mean_accuracy = []

    for subtext in subtexts:
        total_iterations = 0
        for _ in range(n_iterations):
            cipher = cipher_generator.generate_cipher()
            encoded_text = text_encoder.encode_text(subtext, cipher)

            # Initialize a code breaker for that encoded message
            cipher_breaker_nstart = CipherBreaker(
                cipher_generator=cipher_generator,
                ciphered_text=encoded_text,
                probability_table=probability_matrix.probability_table,
            )

            # Break the code and store the extract_top in a dictionary (avoid printing)
            cipher_breaker_nstart.break_cipher_nstart(
                iterations=max_iterations, print_interval=max_iterations, nstart=nstart
            )
            best_dict = cipher_breaker_nstart.extract_best(
                n_extract=extract_top, return_likelihood=True
            )

            # Extract only the text and store it in a list
            best_dict_text = [t[0] for t in best_dict]
            print(best_dict_text)

            # Now we check the percentage of correct ones in the string we matched the most with
            total_iterations = total_iterations + max(
                [
                    similar(subtext, best_dict_text[l])
                    for l in range(len(best_dict_text))
                ]
            )

        mean_accuracy.append(total_iterations / n_iterations)

    return mean_accuracy


import matplotlib.pyplot as plt
import numpy as np


def barplot(accuracy_data, lengths, titles, bar_width=0.2):
    # Set the width of each bar
    bar_width = bar_width

    # Set the positions of the bars on the x-axis
    x_pos = np.arange(len(lengths))

    # Define the colors for each text
    colors = ["r", "g", "b", "c", "m", "y", "k"]

    # Plot the results using a bar plot
    for i, accuracies in enumerate(accuracy_data):
        plt.bar(
            x_pos + (i - len(accuracy_data) / 2) * bar_width,
            accuracies,
            bar_width,
            color=colors[i],
            label=titles[i],
        )

    # Add labels, title, and legend
    plt.xlabel("Number of words")
    plt.ylabel("% of letters decrypted correctly")
    plt.title("Decryption Accuracy by Text Length")
    plt.xticks(x_pos, lengths)
    plt.legend()

    # Adjust layout and spacing for better appearance
    plt.tight_layout()
    plt.grid(True, linestyle="--", alpha=0.5)

    # Display the plot
    plt.show()


import matplotlib.pyplot as plt
import numpy as np


def plot_accuracy_by_length(accuracy_data, lengths, titles):
    # Set up the plot
    fig, ax = plt.subplots()

    # Define colors for each line
    colors = ["r", "g", "b", "c", "m", "y", "k"]

    # Plot the lines and scatter points
    for i, accuracies in enumerate(accuracy_data):
        ax.plot(lengths, accuracies, linestyle="--", color=colors[i], label=titles[i])
        ax.scatter(lengths, accuracies, color=colors[i])

    # Set labels and title
    ax.set_xlabel("Number of words")
    ax.set_ylabel("% of letters decrypted correctly")
    ax.set_title("Decryption Accuracy by Text Length")

    # Add grid
    ax.grid(True, linestyle="--", alpha=0.5)

    # Add legend
    ax.legend()

    # Show the plot
    plt.show()
