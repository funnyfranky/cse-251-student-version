"""
Course: CSE 251 
Lesson: L04 Prove
File:   prove.py
Author: <Add name here>

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- Complete the assignments TODO sections and DO NOT edit parts you were told to leave alone.
- Review the full instructions in Canvas; there are a lot of DO NOTS in this lesson.
"""

import time
import threading
import random
from datetime import datetime

# Include cse 251 common Python files
from cse251 import *

# Global Constants - DO NOT CHANGE
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has was just created in the terminal
        print(f'Created: {self.info()}')
           
    def info(self):
        """ Helper function to quickly get the car information. """
        return f'{self.make} {self.model}, {self.year}'


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.__items = []

    def size(self):
        return len(self.__items)

    def put(self, item):
        assert len(self.__items) <= 10
        self.__items.append(item)

    def get(self):
        return self.__items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, queue, empty_slots, available_cars, queue_lock):
        threading.Thread.__init__(self)
        self.queue = queue
        self.empty_slots = empty_slots
        self.available_cars = available_cars
        self.queue_lock = queue_lock

    def run(self):
        for _ in range(CARS_TO_PRODUCE):
            self.empty_slots.acquire()  # Wait for an empty slot

            car = Car()  # Create a car

            with self.queue_lock:  # Ensure thread safety
                self.queue.put(car)

            self.available_cars.release()  # Signal that a car is available

        # Signal dealer that production is complete
        self.available_cars.release()

class Dealer(threading.Thread):
    """ This is a dealer that receives cars """
    def __init__(self, queue, empty_slots, available_cars, queue_lock, queue_stats):
        threading.Thread.__init__(self)
        self.queue = queue
        self.empty_slots = empty_slots
        self.available_cars = available_cars
        self.queue_lock = queue_lock
        self.queue_stats = queue_stats

    def run(self):
        while True:
            self.available_cars.acquire()  # Wait for a car to be available

            with self.queue_lock:  # Ensure thread safety
                if self.queue.size() == 0:
                    break  # Stop if no more cars to process
                car = self.queue.get()
                self.queue_stats[self.queue.size()] += 1  # Track queue length

            self.empty_slots.release()  # Signal that a slot is now free

            print(f'Sold: {car.info()}')
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

def main():
    log = Log(show_terminal=True)

    # TODO Create semaphore(s)
    empty_slots = threading.Semaphore(MAX_QUEUE_SIZE)  # Initially all slots empty
    available_cars = threading.Semaphore(0)  # Initially no cars available

    # TODO Create queue251 
    # TODO Create lock(s) ?

    queue = Queue251()
    queue_lock = threading.Lock()

    # This tracks the length of the car queue during receiving cars by the dealership
    queue_stats = [0] * MAX_QUEUE_SIZE

    factory = Factory(queue, empty_slots, available_cars, queue_lock)
    dealer = Dealer(queue, empty_slots, available_cars, queue_lock, queue_stats)

    log.start_timer()

    # Start threads
    factory.start()
    dealer.start()

    # Wait for threads to complete
    factory.join()
    dealer.join()

    log.stop_timer(f'All {sum(queue_stats)} have been created')

    xaxis = [i for i in range(0, MAX_QUEUE_SIZE)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count', filename='Production count vs queue size.png')



if __name__ == '__main__':
    main()