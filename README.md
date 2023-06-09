# HMM-for-text-decryption

**[Here](main.ipynb) is th algorithm descrybed by Diaconis in [this](articles/MCMCRev.pdf) article.**

This repository contains *(for now)* a Python implementation of a MCMC method useful for text decryption.
The method is applied for decrypting messages which have been encoded using a substitution cipher.

## Repository description

- [src](src/) contains the definition of the classes written from scratch.

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
        The Probability Matrix is a Python class designed to compute the probability matrix for two-character sequences in a given text. It offers methods for computing the probability table, retrieving the probability of a specific sequence, and saving the computed data to files.


    - [CipherBreaker.py](src/CipherBreaker.py) \
        The Cipher Breaker is a Python class that aims to break a given cipher by performing iterations of swapping elements in the current cipher. It uses a probability table, a decoder, and a likelihood calculator to evaluate the quality of each proposed cipher during the breaking process. The class also provides functionality to generate an animation of the breaking process.
    
- [texts](texts/) contains the texts used to learn the transition probabilities.

- [outputs](outputs/) contains some ```.txt``` outputs from [main.ipynb](main.ipynb).

- [GIF](GIF/) contains ```.gif``` outputs from [main.ipynb](main.ipynb).

## Example

The following gifs are the result of running [main.ipynb](main.ipynb) with different text.

Original Text: *she is not acting by design as yet she cannot even be certain of the degree of her own regard nor of its reasonableness she has known him only a fortnight she danced four dances with him at meryton she saw him one morning at his own house and has since dined in company with him four times*

![](GIF/she%20is%20not.gif)


Original Text: *your plan is a good one replied elizabeth where nothing is in question but the desire of being well married and if i were determined to get a rich husband or any husband i dare say i should adopt it but these are not jane s feelings*

![](GIF/your%20plan.gif)


Original Text: *there were better sense in the sad mechanic exercise of determining the reason of its absence where it is not in the novels of the last hundred years there are vast numbers of young ladies with whom it might be a pleasure to fall in love there are at least five with whom as it seems to me no man of taste and spirit can help doing so*


![](GIF/there%20were.gif)

## To do

- HMM

## Last big updates

CipherBreaker ora ha come attribute history, un dizionario che ha come keys i testi decriptati a ogni iterazione e con value la log likelihood, in questo modo possimo estrarceli tutti.
