import string


def map_alphabet_to_numbers():
    """
    Maps each character in the alphabet to a corresponding number.

    Returns:
        dict: A dictionary where characters are keys and their corresponding numbers are values.
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz "
    mapping = {char: i for i, char in enumerate(alphabet)}
    return mapping


def string_to_numbers(text, mapping):
    """
    Converts a string of characters to a list of numbers based on the provided mapping.

    Args:
        text (str): The input string to be converted.
        mapping (dict): A dictionary mapping characters to numbers.

    Returns:
        list: A list of numbers representing the characters in the input string.
    """
    numbers = [mapping[char] for char in text]
    return numbers


def find_mapping(L):
    """
    Creates a mapping between indices and characters based on the given list of numbers.

    Args:
        L (list): A list of numbers representing indices.

    Returns:
        dict: A dictionary mapping each character from the alphabet to its corresponding character in the given list.
    """
    alphabet = string.ascii_lowercase + " "
    mapping = {}
    for i, num in enumerate(L):
        mapping[alphabet[i]] = alphabet[num]
    return mapping


def numbers_to_string(string, mapping):
    """
    Converts a list of numbers back into a string using the provided mapping.

    Args:
        string (list): A list of numbers representing characters.
        mapping (dict): A dictionary mapping characters to their corresponding characters.

    Returns:
        str: The transformed string.
    """
    transformed_string = ""
    for char in string:
        if char in mapping:
            transformed_string += mapping[char]
        else:
            transformed_string += char
    return transformed_string


def invert_mapping(mapping):
    """
    Inverts the given mapping, swapping keys with values.

    Args:
        mapping (dict): A dictionary mapping characters to their corresponding characters.

    Returns:
        dict: A dictionary with the values of the original mapping as keys and the keys as values.
    """
    inverted_mapping = {value: key for key, value in mapping.items()}
    return inverted_mapping
