#!/usr/bin/python
# coding=utf-8

import argparse
import codecs
import random
import sys

parser = argparse.ArgumentParser(description="""A tool to help memorize some
text! When provided with a file, this program will remove random words from
each line of text and ask you to provide the words that were removed.""")

parser.add_argument('--no-color', action='store_true',
                    help='hide colorful underlining')

parser.add_argument('--a', dest='tries', default=3,
                    help=('number of tries to allow per word '
                         '(0 for unlimited tries, default: 3)'))

parser.add_argument('--n', dest='num', default=0,
                    help=('number of words to remove from each line '
                         '(0 for random number of removals, default: 0)'))

parser.add_argument('filename', metavar='filename', type=str,
                    help='the text file')

args = parser.parse_args()

try:
    with codecs.open(args.filename, 'r', 'utf-8') as f:
        current_line = ''

        for line in f:
            missing_words = []
            new_word = u''
            split_line = line.split(' ')

            if int(args.num):
                num = int(args.num)
            else:
                #num is in the range [1,len(split_line)], so at least
                #one word will be removed.
                num = random.randrange(len(split_line))+1

            words = [False]*num
            diff = len(split_line)-num
            if diff > 0:
                words.extend([True]*diff)
                random.shuffle(words)

            for i, word in enumerate(split_line):
                show_word = words[i]

                for char in word:
                    if (char.isalpha() and show_word) or not char.isalpha():
                        current_line += char
                    else:
                        new_word += char

                        if not args.no_color:
                            current_line += '\033[91m'

                        current_line += '_'

                        if not args.no_color:
                            current_line += '\033[0m'
                if word[-1] != '\n':
                    current_line += ' '

                if len(new_word):
                    missing_words.append(new_word)
                    new_word = u''
            tries = 0

            while len(missing_words):
                
                next_word = missing_words[0]
                print(current_line)

                try:
                    guess = raw_input('Enter the next missing word: ')
                except KeyboardInterrupt:
                    sys.exit(0)

                if unicode(guess,'utf-8') == next_word:
                    print("Correct! The word was '" + next_word + "'.")
                elif args.tries and tries == args.tries:
                    print("Too many tries. The word was '" + next_word + "'.")
                else:
                    print("Incorrect. Please try again.")
                    tries += 1
                    continue

                if args.no_color:
                    current_line = current_line.replace('_' * len(next_word),next_word,1)
                else:
                    current_line = current_line.replace('\033[91m_\033[0m' * len(next_word),next_word,1)

                missing_words.pop(0)
                tries = 0
except IOError:
    print("File not found: '{}'".format(args.filename))
