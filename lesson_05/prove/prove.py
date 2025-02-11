"""
Course: CSE 251 
Lesson: L05 Prove
File:   prove.py
Author: Josh Chapman

Purpose: Assignment 05 - Factories and Dealers

Instructions:

- Read the comments in the following code.  
- Implement your code where the TODO comments are found.
- No global variables, all data must be passed to the objects.
- Only the included/imported packages are allowed.  
- Thread/process pools are not allowed
- You MUST use a barrier!
- Do not use try...except statements.
- You are not allowed to use the normal Python Queue object. You must use Queue251.
- The shared queue between the threads that are used to hold the Car objects
  can not be greater than MAX_QUEUE_SIZE.
"""

from datetime import datetime, timedelta
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Constants.
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
        # print(f'Created: {self.info()}')
           
    def info(self):
        """ Helper function to quickly get the car information. """
        return f'{self.make} {self.model}, {self.year}'


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.__items = []
        self.__max_size = 0

    def get_max_size(self):
        return self.__max_size

    def put(self, item):
        self.__items.append(item)
        if len(self.__items) > self.__max_size:
            self.__max_size = len(self.__items)

    def get(self):
        return self.__items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self,queue,empty_slots,available_cars,queue_lock,barrier): # factory_list
        threading.Thread.__init__(self)
        self.cars_to_produce = random.randint(200, 300) # DO NOT change
        self.queue = queue
        self.empty_slots = empty_slots
        self.available_cars = available_cars
        self.queue_lock = queue_lock
        self.barrier = barrier
        # self.factory_list = factory_list


    def run(self):
        # TODO produce the cars, the send them to the dealerships
        for _ in range(self.cars_to_produce):
            self.empty_slots.acquire()

            car = Car()

            with self.queue_lock:
                self.queue.put(car)

            self.available_cars.release()
        # TODO wait until all of the factories are finished producing cars
        self.barrier.wait()
        # TODO "Wake up/signal" the dealerships one more time.  Select one factory to do this
        # if self is self.factory_list[0]:  # Check if this is the first factory
        #     for _ in range(len(self.factory_list)):  # One None per dealer
        #         with self.queue_lock:
        #             self.queue.put(None)
        #         self.available_cars.release()



class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self,queue,empty_slots,available_cars,queue_lock):
        threading.Thread.__init__(self)
        self.queue = queue
        self.empty_slots = empty_slots
        self.available_cars = available_cars
        self.queue_lock = queue_lock
        self.dealer_stats = 0

    def run(self):
        while True:
            self.available_cars.acquire()
            # car = self.queue.get()

            with self.queue_lock:
                car = self.queue.get()
                if car is None:
                    break

            self.dealer_stats += 1
            self.empty_slots.release()

            # print(f'Sold: {car.info()}')

            # Sleep a little - don't change.  This is the last line of the loop
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR + 0))



def run_production(factory_count, dealer_count):
    """ This function will do a production run with the number of
        factories and dealerships passed in as arguments.
    """

    # Create semaphore(s) if needed
    empty_slots = threading.Semaphore(MAX_QUEUE_SIZE)
    available_cars = threading.Semaphore(0)

    # Create queue
    car_queue = Queue251()

    # TODO Create lock(s) if needed
    lock = threading.Lock()

    # TODO Create barrier
    barrier = threading.Barrier(factory_count)

    # This is used to track the number of cars received by each dealer
    dealer_stats = list([0] * dealer_count)

    # TODO create your factories, each factory will create a random amount of cars; your code must account for this.
    # NOTE: You have no control over how many cars a factory will create in this assignment.
    factory_list = [Factory(car_queue,empty_slots,available_cars,lock,barrier) for _ in range(factory_count)]    
    
    # factory_list = []
    # factory = Factory(car_queue,empty_slots,available_cars,lock,barrier,factory_list)

    # for _ in range(factory_count):
    #     factory_list.append(factory)

    # TODO create your dealerships
    dealer_list = [Dealer(car_queue,empty_slots,available_cars,lock) for _ in range(dealer_count)]


    # dealer_list = []
    # dealer = Dealer(car_queue,empty_slots,available_cars,lock)

    # for _ in range(dealer_count):
    #     dealer_list.append(dealer)

    log.start_timer()

    # TODO Start all dealerships
    for i in dealer_list:
        i.start()

    # TODO Start all factories
    for i in factory_list:
        i.start()

    # This is used to track the number of cars produced by each factory NOTE: DO NOT pass this into
    # your factories! You must collect this data here in `run_production` after the factories are finished.
    factory_stats = []
    # TODO Wait for the factories and dealerships to complete; do not forget to get the factories stats
    for factory in factory_list:
        factory.join()
        factory_stats.append(factory.cars_to_produce)

    for _ in range(dealer_count):
        with lock:
            car_queue.put(None)
        available_cars.release()

    i = 0
    for dealer in dealer_list:
        dealer.join()
        dealer_stats[i] = dealer.dealer_stats
        i += 1






    run_time = log.stop_timer(f'{sum(dealer_stats)} cars have been created.')

    # This function must return the following - Don't change!
    # factory_stats: is a list of the number of cars produced by each factory.
    #                collect this information after the factories are finished. 
    return (run_time, car_queue.get_max_size(), dealer_stats, factory_stats)


def main(log):
    """ Main function - DO NOT CHANGE! """

    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for factories, dealerships in runs:
        run_time, max_queue_size, dealer_stats, factory_stats = run_production(factories, dealerships)

        log.write(f'Factories      : {factories}')
        log.write(f'Dealerships    : {dealerships}')
        log.write(f'Run Time       : {run_time:.4f}')
        log.write(f'Max queue size : {max_queue_size}')
        log.write(f'Factory Stats  : Made = {sum(dealer_stats)} @ {factory_stats}')
        log.write(f'Dealer Stats   : Sold = {sum(factory_stats)} @ {dealer_stats}')
        log.write('')

        # The number of cars produces needs to match the cars sold
        assert sum(dealer_stats) == sum(factory_stats)


if __name__ == '__main__':
    log = Log(show_terminal=True)
    main(log)