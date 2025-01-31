"""
Course: CSE 251
Lesson Week: 03
File: coding.py
Author: Brother Comeau
"""

import time
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np

from cse251 import *

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def worker(value):
    # only process 1 number
    if is_prime(value):
        return(value)
    else:
        return -1

def main():
    global prime_count
    log = Log(show_terminal=True)
    log.start_timer()

    start = 10000000000
    range_count = 100000

    # must create a list of ALL data for the map()
    data = [ i for i in range(start, start + range_count) ]

    # create a pool of 6 workers to process all values in data
    with mp.Pool(6) as p:
        results = p.map(worker, data)

    # filter the results to remove -1 values
    answer = list(filter(lambda x: x > 0, results))

    # Should find 4306 primes
    log.write(f'{answer}')
    log.write(f'Numbers processed = {len(data)}')
    log.write(f'Primes found      = {len(answer)}')
    log.stop_timer('Total time')


if __name__ == '__main__':
    main()
