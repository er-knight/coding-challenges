# [The Challenge - Building A Huffman Encoder/Decoder](https://codingchallenges.fyi/challenges/challenge-huffman)

In the early 1950s David Huffman developed an algorithm to find the optimal prefix code that can be used for lossless data compression.

Given there is usually an unequal distribution of character occurrences in text this can then be used to compress data by giving the most commonly occurring characters the shortest prefix.

For example if we have the string aaabbc, it would normally take up 6 bytes, but if we assign each character a variable length code, with the most frequently occurring character has the shortest code we might give them the following codes:
```
a: 1
b: 01
c: 10
```
and we could reduce the string aaabbc (six bytes) to `111010110` (nine bits). It’s not quite that simple though as we need to ensure that the codes are prefix-free, that is the bit string representing one character is not a prefix of a bit string representing another.

These prefix-free codes are generated by creating a binary tree. Before we get into that let’s consider the steps involved in compression using Huffman Codes:

1. Read the text and determine the frequency of each character occurring.
2. Build the binary tree from the frequencies.
3. Generate the prefix-code table from the tree.
4. Encode the text using the code table.
5. Encode the tree - we’ll need to include this in the output file so we can decode it.
6. Write the encoded tree and text to an output field

## Usage
- Compress
```sh
./main.py -c -f file-name.txt 
```
- Decompress
```sh
./main.py -d -f file-name.huff 
```
