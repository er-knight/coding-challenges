import sys
import argparse

from pathlib import Path

def main():

    parser = argparse.ArgumentParser(
        prog='python main.py', 
        description='Print newline, word, and byte counts for each FILE,' 
                    ' and a total line if more than one FILE is specified.'
                    ' A word is a non-zero-length sequence of characters'
                    'delimited by white space.'
    )
    parser.add_argument('-c', '--bytes', action='store_true', help='print the byte counts')
    parser.add_argument('-m', '--chars', action='store_true', help='print the character counts')
    parser.add_argument('-l', '--lines', action='store_true', help='print the newline counts')
    parser.add_argument('-w', '--words', action='store_true', help='print the word counts')
    parser.add_argument('FILE', action='store')

    args = parser.parse_args()

    file_to_read = Path().cwd() / args.FILE
    chars = words = newlines = bytes_count = 0 
    with file_to_read.open('rb') as f:
        _bytes = f.read()
        bytes_count = len(_bytes)

    prev_char = ''
    for char in _bytes.decode():
        if char == '\n':
            newlines += 1
            prev_char = ''
        elif char.strip():
            prev_char = char
        else:
            if prev_char:
                words += 1
            prev_char = ''
        chars += 1

    if prev_char:
        words += 1

    output = []
    if not any((args.bytes, args.chars, args.lines, args.words)):
        output.extend([newlines, words, bytes_count])
    else:
        if args.lines:
            output.append(newlines)
        if args.words:
            output.append(words)
        if args.chars:
            output.append(chars)
        if args.bytes:
            output.append(bytes_count)

    width = max([len(str(i)) for i in output])
    output = [str(i).rjust(width) for i in output]

    print(*output, args.FILE)

if __name__ == '__main__':

    main()