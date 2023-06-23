# HMM-for-text-decryption

This repository contains Python implementation of a MCMC and HMM methods for text decryption.
The method is applied for decrypting messages which have been encoded using substitution cipher, homophonic cipher an double cipher.

**[Here](Decription using HMM.pdf) there is the outline of our project.**
## Repository description

- [src](src/) contains the implementation of the algorithms and other functions needed for preprocessing and evaluattion written from scratch.

    - [CipherUtils.py](src/CipherUtils.py) 
        - Cipher Generator \
            The Cipher Generator is a Python class that allows you to generate a random cipher. A cipher is essentially a shuffled version of the alphabet. This class provides a method called generate_cipher() that returns a list representing the generated cipher.

        - Text Encoder \
            The Text Encoder is a Python class that provides functionality to encode text using a given cipher. It has a method called encode_text(text, cipher) that takes an input text and a cipher as parameters and returns the encoded text as a string.

        - Text Decoder \
            The Text Decoder is a Python class that enables the decoding of encoded text using a provided cipher. It contains a method called decode_text(text, cipher) that takes an encoded text and a cipher as input and returns the decoded text as a string.

        - Text Preprocessor \
            The Text Preprocessor is a Python class that performs preprocessing operations on text. It provides methods for converting text to lowercase, finding unknown characters in the text, removing unknown characters from the text, removing extra-spaces, and saving the preprocessed text to a file.

    - [ProbabilityMatrix.py](src/ProbabilityMatrix.py) \
            Probability Matrix is a class used to compute the probability table and the probability matrix for all bigrams within a given text. It is used both for MCMC and HMM approach.
      
    - MCMC
        - [CipherBreaker.py](src/CipherBreaker.py) \
            The Cipher Breaker is a Python class that aims to break a given cipher by performing iterations of swapping elements in the current cipher using MCMC eexploration. It uses a probability table, a decoder, and a likelihood calculator to evaluate the quality of each proposed cipher during the breaking process. The class also provides functionality to generate an animation of the breaking process.
    - HMM
      - [HMM_functions.py](src/HMM_functions.py) \
            Contains Baum-Welch algorithm and Viterbi algorithm implementation.
      - [HMM_utils.py](src/HMM_utils.py) \
            This module provides functions to map characters in the alphabet to corresponding numbers, convert strings to lists of numbers based on a given mapping, create mappings between indices and characters.

    - [evaluation.py](src/evaluation.py) \
            This module provides functions for MCMC and HMM performances comparison.
    
        
      
    
    
- [texts](texts/) contains the corpus used to learn the transition probabilities.

- [outputs](outputs/) contains:
    - accuracies coming from evaluation modules.
    - probability matrix of bigrams computed using the corpus.

- [GIF](GIF/) contains ```.gif``` outputs from [main.ipynb](main.ipynb).
- [Articles](articles/) contains some interesting articles about the topic.

## Example

The following gifs are the result of running [main.ipynb](main.ipynb) with different text.

Original Text: *she is not acting by design as yet she cannot even be certain of the degree of her own regard nor of its reasonableness she has known him only a fortnight she danced four dances with him at meryton she saw him one morning at his own house and has since dined in company with him four times*

![](GIF/she%20is%20not.gif)


Original Text: *your plan is a good one replied elizabeth where nothing is in question but the desire of being well married and if i were determined to get a rich husband or any husband i dare say i should adopt it but these are not jane s feelings*

![](GIF/your%20plan.gif)


Original Text: *there were better sense in the sad mechanic exercise of determining the reason of its absence where it is not in the novels of the last hundred years there are vast numbers of young ladies with whom it might be a pleasure to fall in love there are at least five with whom as it seems to me no man of taste and spirit can help doing so*


![](GIF/there%20were.gif)

