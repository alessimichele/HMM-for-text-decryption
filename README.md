# HMM-for-text-decryption

**[Qui](try.ipynb) c'è una prova dell'idea dell'algoritmo descritto da [Diaconis](articles/MCMCRev.pdf), che non funziona**

This repository contains (for now) two Python classes that are useful for text decryption using Hidden Markov Models (HMMs).

- [Probability.py](src/Probability.py) is a class that computes transition probabilities based on a given text and alphabet. It provides methods to compute the probability matrix, retrieve individual probabilities, and print the computed probabilities. The class helps in analyzing the statistical patterns of character transitions in the text.
Example:
Most likely couple of world inside Moby Dick text:
```
p(t|h) = 0.04275806212268933
p(h|e) = 0.03614000002773706
p(i|n) = 0.02706443457313361
p(a|n) = 0.020653013562034625
p(e|r) = 0.020310460892828168
p(r|e) = 0.015982092955203264
p(h|a) = 0.0157324594310852
p(n|d) = 0.014948887535936825
p(a|t) = 0.014005827555935244
p(n|g) = 0.01365772747508172
p(h|i) = 0.01308357036961017
p(o|n) = 0.012614814085432913
p(e|d) = 0.012610653526697612
p(e|n) = 0.012161313183285094
p(s|t) = 0.011879782042196387
```
- [AlphabetPermutation.py](src/AlphabetPermutation.py)  is a class that facilitates text encryption. Given an alphabet, it generates a permutation of the characters and provides a method to encrypt text using the generated permutation.
Example:
```
Permutation:
a -> u
b -> i
c -> v
d -> o
e -> x
f -> n
g -> q
h -> m
i -> g
j -> h
k -> d
l -> w
m -> c
n -> s
o -> b
p -> y
q -> a
r -> f
s -> p
t -> l
u -> j
v -> z
w -> r
x -> k
y -> e
z -> t
Original string: hello world
Permuted string: mxwwb rbfwo
```