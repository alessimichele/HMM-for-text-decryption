# HMM-for-text-decryption

**[Qui](main.ipynb) c'è l'algoritmo descritto da [Diaconis](articles/MCMCRev.pdf), che FUNZIONA!**

This repository contains (for now) a Python implementation of a MCMC method useful for text decryption.

CipherBreaker ora ha come attribute history, un dizionario che ha come keys i testi decriptati a ogni iterazione e con value la log likelihood, in questo modo possimo estrarceli tutti.

- [CipherBreaker.py](src/CipherBreaker.py) 
    - Cipher Generator
        The Cipher Generator is a Python class that allows you to generate a random cipher. A cipher is essentially a shuffled version of the alphabet. This class provides a method called generate_cipher() that returns a list representing the generated cipher.

    - Text Encoder
        The Text Encoder is a Python class that provides functionality to encode text using a given cipher. It has a method called encode_text(text, cipher) that takes an input text and a cipher as parameters and returns the encoded text as a string.

    - Text Decoder
        The Text Decoder is a Python class that enables the decoding of encoded text using a provided cipher. It contains a method called decode_text(text, cipher) that takes an encoded text and a cipher as input and returns the decoded text as a string.

    - Text Preprocessor
        The Text Preprocessor is a Python class that performs preprocessing operations on text. It provides methods for converting text to lowercase, finding unknown characters in the text, removing unknown characters from the text, removing extra-spaces, and saving the preprocessed text to a file.



- [ProbabilityMatrix.py](src/ProbabilityMatrix.py) 
    The Probability Matrix is a Python class designed to compute the probability matrix for two-character sequences in a given text. It offers methods for computing the probability table, retrieving the probability of a specific sequence, and saving the computed data to files.


- [CipherBreaker.py](src/CipherBreaker.py) 
    The Cipher Breaker is a Python class that aims to break a given cipher by performing iterations of swapping elements in the current cipher. It uses a probability table, a decoder, and a likelihood calculator to evaluate the quality of each proposed cipher during the breaking process. The class also provides functionality to generate an animation of the breaking process.

# Example

The following gifs are the result of running [main.ipynb](main.ipynb) with different text.

![](GIF/she%20is%20not.gif)

![](GIF/your%20plan.gif)

![](GIF/your%20plan.gif)
