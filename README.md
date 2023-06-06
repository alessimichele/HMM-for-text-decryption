# HMM-for-text-decryption

This repository contains (for now) two Python classes that are useful for text decryption using Hidden Markov Models (HMMs).

- [Probability.py](src/Probability.py) is a class that computes transition probabilities based on a given text and alphabet. It provides methods to compute the probability matrix, retrieve individual probabilities, and print the computed probabilities. The class helps in analyzing the statistical patterns of character transitions in the text.

- [AlphabetPermutation.py](src/AlphabetPermutation.py)  is a class that facilitates text encryption. Given an alphabet, it generates a permutation of the characters and provides a method to encrypt text using the generated permutation.