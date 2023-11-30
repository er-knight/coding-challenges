#!/usr/bin/env python
 
import argparse
from dataclasses import dataclass
from math import ceil
from pathlib import Path
from collections import Counter
from heapq import heapify, heappop, heappush
from typing import Self, Union

@dataclass
class Node:
    char: str = ''
    freq: int = 0
    left: Union[Self, None] = None  
    right: Union[Self, None] = None
    code: str = ''

    def __gt__(self, other: Self) -> bool:
        if self.freq == other.freq:
            return self.char > other.char
        return self.freq > other.freq
    
def read_file(file_name: str) -> bytes:
    with (Path().cwd() / file_name).open('rb') as f:
        return f.read()

def write_file(file_name: str, _bytes: bytes) -> None:
    with (Path().cwd() / file_name).open('wb') as f:
        f.write(_bytes)

def count_frequencies(_str: str) -> Counter:
    return Counter(_str)

def generate_tree(frequencies: Counter) -> Node:

    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapify(heap)
    
    while len(heap) > 1:
        first, second = heappop(heap), heappop(heap)
        heappush(heap, Node('', first.freq + second.freq, first, second))

    return heappop(heap)

def generate_prefix_codes(root_node: Node) -> dict[str, str]:

    prefix_codes = {}

    stack = [root_node]
    while stack:
        node = stack.pop()
        if node.char:
            prefix_codes[node.char] = node.code

        if node.left:
            left_node = node.left
            left_node.code = node.code + '0'
            stack.append(left_node)
            
        if node.right:
            right_node = node.right
            right_node.code = node.code + '1'
            stack.append(right_node)

    return prefix_codes

def tree_to_bytes(root_node: Node) -> bytes:
    """
    convert binary tree to sequence of bits (0s and 1s) using postorder traversal
    where, 0 for non-leaf node and 1 for leaf node.
    
    why postorder: https://engineering.purdue.edu/ece264/17au/hw/HW13?alt=huffman
    """

    bytes_array = []
    bits_required = 0
    chars = []
    
    def to_postorder(root: Node) -> None:
        if root:
            to_postorder(root.left)
            to_postorder(root.right)
            bit = 0 if root.left or root.right else 1
            if root.char:
                chars.append(root.char)
            nonlocal bits_required
            if bits_required % 8 == 0:
                bytes_array.append(bit)
            else:
                bytes_array[-1] = bytes_array[-1] << 1 | bit
            bits_required += 1


    to_postorder(root_node)

    if bits_required % 8 != 0:
        bytes_array[-1] = bytes_array[-1] << (8 - (bits_required % 8))

    return (bytes(bytes_array), bits_required, ''.join(chars[::-1]))

def bytes_to_tree(_bytes: bytes, size: int, chars: str) -> Node:
    char_index = 0
    bits = list(''.join(map(lambda b: bin(b)[2:].rjust(8, '0'), _bytes))[:size])

    def from_postorder() -> Union[Node, None]:
        if bits:
            node = Node()
            if bits.pop() == '0':
                node.right = from_postorder()
                node.left = from_postorder()
            else:
                nonlocal char_index
                node = Node(char=chars[char_index])
                char_index += 1
            return node
    
    return from_postorder()

def compress(_str: str, prefix_codes: dict[int, int]) -> tuple[bytes, int]:
    """returns `__str` encoded as `bytes` and number of actual bit required"""

    bytes_array = []
    bits_required = 0
    for char in _str:
        for bit in map(int, prefix_codes[char]):
            if bits_required % 8 == 0:
                bytes_array.append(bit)
            else:
                bytes_array[-1] = bytes_array[-1] << 1 | bit
            bits_required += 1

    if bits_required % 8 != 0:
        bytes_array[-1] = bytes_array[-1] << (8 - (bits_required % 8))

    return (bytes(bytes_array), bits_required)

def decompress(_bytes: bytes, size: int, tree: Node) -> bytes:

    _str = []
    bits = ''.join(map(lambda b: bin(b)[2:].rjust(8, '0'), _bytes))[:size]

    i = 0
    stack = [tree]
    while stack:
        node = stack.pop()
        if node.char:
            _str.append(node.char)
            stack = [tree]
        elif i < len(bits):
            if bits[i] == '0':
                stack.append(node.left)
            else: # bits[i] == '1'
                stack.append(node.right)
            i += 1

    return ''.join(_str).encode()

def main() -> None:

    parser = argparse.ArgumentParser()
    action_parser = parser.add_mutually_exclusive_group(required=True)
    action_parser.add_argument('-c', '--compress', action='store_true')
    action_parser.add_argument('-d', '--decompress', action='store_true')
    parser.add_argument('-f', '--file', required=True)

    args = parser.parse_args()
    file_name = args.file

    if args.compress:

        file_content = read_file(file_name).decode()
        frequencies = count_frequencies(file_content)
        tree = generate_tree(frequencies)

        tree_as_bytes, size, chars = tree_to_bytes(tree)
        header = len(chars.encode()).to_bytes(4)
        header += (size).to_bytes(4)

        prefix_codes = generate_prefix_codes(tree)
        compressed_content, size = compress(file_content, prefix_codes)

        header += (size).to_bytes(4)
        header += chars.encode()
        header += tree_as_bytes
        
        file_name = file_name.removesuffix('.txt') + '.huff'
        write_file(file_name, header + compressed_content)
        print('saved to', file_name)

    else:

        file_content = read_file(file_name)

        chars_size = int.from_bytes(file_content[0:4])
        tree_size_in_bits = int.from_bytes(file_content[4:8])
        content_size_in_bits = int.from_bytes(file_content[8:12])

        chars = file_content[12:12 + chars_size].decode()
        tree_as_bytes = file_content[12 + chars_size:12 + chars_size + ceil(tree_size_in_bits / 8.0)]
        tree = bytes_to_tree(tree_as_bytes, tree_size_in_bits, chars)

        compressed_content = file_content[12 + chars_size + ceil(tree_size_in_bits / 8.0):]

        decompressed_content = decompress(compressed_content, content_size_in_bits, tree)

        file_name = file_name.removesuffix('.huff') + '.txt'
        write_file(file_name, decompressed_content)
        print('saved to', file_name)

if __name__ == "__main__":

    main()