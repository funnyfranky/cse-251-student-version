"""
Course: CSE 251
Lesson Week: 10
File: team2.py
Author: Brother Comeau
Instructions:
- Look for the TODO comments

The Python function ord() will help you.

"""

import time
import threading
import random
import string
import os

# -----------------------------------------------------------------------------
def reverse_file_non_mmap(filename):
    """ Display a file in reverse order NOT using MMAP 
        The last char will be displayed first, then the second
        last char will be next, etc...
    """
    # TODO add code here
    with open(filename, "r") as myfile:
        data = myfile.read()

    f1 = open(filename, "w")

    data_1 = data[::-1]

    f1.write(data_1)

    f1.close()


# -----------------------------------------------------------------------------
def reverse_file(filename):
    """ Display a file in reverse order USING a mmap file. 
        The last char will be displayed first, then the second
        last char will be next, etc...
    """
    # TODO add code here
    pass


# -----------------------------------------------------------------------------
def promote_letter_a(filename):
    """ 
    change the given file with these rules:
    1) when the letter is 'a', uppercase it
    2) all other letters are changed to the character '.'

    You are not creating a different file.  Change the file using mmap file.
    """
    # TODO add code here
    pass


# -----------------------------------------------------------------------------
def promote_letter_a_threads(filename):
    """ 
    change the given file with these rules:
    1) when the letter is 'a', uppercase it
    2) all other letters are changed to the character '.'

    You are not creating a different file.  Change the file using mmap file.

    Use N threads to process the file where each thread will be 1/N of the file.
    """
    # TODO add code here
    pass


def create_large_file(filename):
    if not os.path.exists(filename):
        print('Creating large data file', end='')
        words = []

        for _ in range(1000):
            word = ''
            for _ in range(80):
                word += random.choice(string.ascii_lowercase)
            words.append(word)

        with open(filename, 'w') as f:
            for i in range(2000000):
                if i % 25000 == 0:
                    print('.', end='', flush=True)

                f.write(random.choice(words))
                f.write('\n')
            print()


# -----------------------------------------------------------------------------
def main():
    # create_large_file('letter_a.txt')

    reverse_file_non_mmap('data.txt')
    # reverse_file('data.txt')

    # promote_letter_a('letter_a.txt')
    
    # TODO
    # When you get the function promote_letter_a() working
    #  1) Comment out the promote_letter_a() call
    #  2) run create_Data_file.py again to re-create the "letter_a.txt" file
    #  3) Uncomment the function below
    # promote_letter_a_threads('letter_a.txt')

if __name__ == '__main__':
    main()
