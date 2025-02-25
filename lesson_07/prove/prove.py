"""
Course: CSE 251 
Lesson: L07 Prove
File:   prove.py
Author: Joshua Chapman

Purpose: Process Task Files.

Instructions:

See Canvas for the full instructions for this assignment. You will need to complete the TODO comment
below before submitting this file:

Note: each of the 5 task functions need to return a string.  They should not print anything.

I ran this code many times and this was the lowest time values I could get it to pull. I gave prime and word functions 2 pools since prime can be doing some heavy calculation, and I gave word 2 since it needed to search about 3 hundred thousand lines in a file for a word. Uppercase and summing weren't intensive functions so they get one pool each. Name got 5 since there's an in/out slowdown and I wanted it to be fast. I wasn't sure how to test other than running it a bunch of times and seeing what was faster and I think I got a great amount of pools.
"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math

# Include cse 251 common Python files - Dont change
from cse251 import *

# Constants - Don't change
TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# TODO: Change the pool sizes and explain your reasoning in the header comment

PRIME_POOL_SIZE = 2
WORD_POOL_SIZE  = 2
UPPER_POOL_SIZE = 1
SUM_POOL_SIZE   = 1
NAME_POOL_SIZE  = 5

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
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

def check_word_in_file(word, fileName):
    with open(fileName, 'r') as file:
        for line in file:
            if word == line.strip():
                return True
        return False

def gaussian_sum(num):
    return num * (num + 1) // 2

def json_to_dictionary(data):
    return json.loads(data.content.decode('utf-8'))


def collect_prime_result(result):
    result_primes.append(result)

def collect_word_result(result):
    result_words.append(result)

def collect_upper_result(result):
    result_upper.append(result)

def collect_sum_result(result):
    result_sums.append(result)

def collect_name_result(result):
    result_names.append(result)


def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    if (is_prime(value)):
        return f'{value} is prime'
    else:
        return f'{value} is not prime'

def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    if check_word_in_file(word, 'words.txt'):
        return f'{word} found'
    else:
        return f'{word} not found'
        


def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    return f'{text} ==>  {text.upper()}'


def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of all numbers between start_value and end_value
        answer = {start_value:,} to {end_value:,} = {total:,}
    """
    return f'sum of all numbers between {start_value} and {end_value}\nanswer = {start_value:,} to {end_value:,} = {gaussian_sum(end_value) - gaussian_sum(start_value)}'


def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    data = requests.get(url)
    dictionary = json_to_dictionary(data)
    if data.status_code == 200:
        return f"{url} has name {dictionary['name']}"
    else:
        return f'{url} had an error receiving the information'



def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    prime_pool = mp.Pool(PRIME_POOL_SIZE)
    word_pool = mp.Pool(WORD_POOL_SIZE)
    upper_pool = mp.Pool(UPPER_POOL_SIZE)
    sum_pool = mp.Pool(SUM_POOL_SIZE)
    name_pool = mp.Pool(NAME_POOL_SIZE)

    # TODO change the following if statements to start the pools
    
    count = 0
    task_files = glob.glob("tasks/*.task")

    for filename in task_files:
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        match task_type:
            case 'prime':
                prime_pool.apply_async(task_prime, args=(task['value'],), callback=collect_prime_result)
            case 'word':
                word_pool.apply_async(task_word, args=(task['word'],), callback=collect_word_result)
            case 'upper':
                upper_pool.apply_async(task_upper, args=(task['text'],), callback=collect_upper_result)
            case 'sum':
                sum_pool.apply_async(task_sum, args=(task['start'], task['end']), callback=collect_sum_result)
            case 'name':
                name_pool.apply_async(task_name, args=(task['url'],), callback=collect_name_result)
            case _:
                log.write(f'Error: unknown task type {task_type}')

    # TODO wait on the pools
    prime_pool.close()
    prime_pool.join()
    sum_pool.close()
    sum_pool.join()
    word_pool.close()
    word_pool.join()
    upper_pool.close()
    upper_pool.join()
    name_pool.close()
    name_pool.join()

    # for filename in task_files:
    #     # print()
    #     # print(filename)
    #     task = load_json_file(filename)
    #     print(task)
    #     count += 1
    #     task_type = task['task']
    #     if task_type == TYPE_PRIME:
    #         task_prime(task['value'])
    #     elif task_type == TYPE_WORD:
    #         task_word(task['word'])
    #     elif task_type == TYPE_UPPER:
    #         task_upper(task['text'])
    #     elif task_type == TYPE_SUM:
    #         task_sum(task['start'], task['end'])
    #     elif task_type == TYPE_NAME:
    #         task_name(task['url'])
    #     else:
    #         log.write(f'Error: unknown task type {task_type}')

    # DO NOT change any code below this line!
    #---------------------------------------------------------------------------
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Total time to process {count} tasks')


if __name__ == '__main__':
    main()