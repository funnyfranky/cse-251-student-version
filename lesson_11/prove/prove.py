"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting(id):
    print(f'Cleaner: {id} waiting...')
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner: {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting(id):
    print(f'Guest: {id} waiting...')
    time.sleep(random.uniform(0, 2))

def guest_partying(id, count):
    print(f'Guest: {id}, count = {count}')
    time.sleep(random.uniform(0, 1))

def cleaner(start_time, cleaner_id, guest_count, clean_count, light_lock, room_lock):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    while start_time + TIME > time.time():
        with room_lock:
            if guest_count.value == 0 and light_lock.acquire(block=False):
                print(STARTING_CLEANING_MESSAGE)
                print(f"Cleaner: {cleaner_id}")
                cleaner_cleaning(cleaner_id)
                print(STOPPING_CLEANING_MESSAGE)
                light_lock.release()
                
                with clean_count.get_lock():
                    clean_count.value += 1
        
        cleaner_waiting(cleaner_id)

def guest(start_time, guest_id, guest_count, parties_count, light_lock, room_lock):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (call guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    while start_time + TIME > time.time():
        with room_lock:
            if guest_count.value == 0:
                light_lock.acquire()  # Turns on light
                print(STARTING_PARTY_MESSAGE)
                with parties_count.get_lock():
                    parties_count.value += 1
            
            with guest_count.get_lock():
                guest_count.value += 1
                guest_number = guest_count.value
        guest_partying(guest_id,guest_number)
        
        with room_lock:
            with guest_count.get_lock():
                guest_count.value -= 1
                if guest_count.value == 0:
                    print(STOPPING_PARTY_MESSAGE)
                    light_lock.release()  # Turns off light
        
        guest_waiting(guest_id)

def main():
    # Start time of the running of the program. 
    start_time = time.time()

    # TODO - add any variables, data structures, processes you need
    room_lock = mp.Lock()
    light_lock = mp.Lock()

    guest_count = mp.Value('i', 0)
    clean_count = mp.Value('i', 0)
    parties_count = mp.Value('i', 0)


    # TODO - add any arguments to cleaner() and guest() that you need
    processes = []
    for i in range(HOTEL_GUESTS):
        p = mp.Process(target=guest, args=(start_time, i, guest_count, parties_count, light_lock, room_lock))
        processes.append(p)
        p.start()
    
    for i in range(CLEANING_STAFF):
        p = mp.Process(target=cleaner, args=(start_time, i, guest_count, clean_count, light_lock, room_lock))
        processes.append(p)
        p.start()
    
    # Wait for all processes to finish
    for p in processes:
        p.join()

    # Results
    cleaned_count = clean_count.value
    party_count = parties_count.value
    print(f'Room was cleaned {cleaned_count} times, there were {party_count} parties')


if __name__ == '__main__':
    main()

