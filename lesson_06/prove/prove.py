"""
Course: CSE 251 
Lesson: L06 Prove
File:   prove.py
Author: Joshua Chapman

Purpose: Processing Plant

Instructions:

- Implement the necessary classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.json'
BOXES_FILENAME   = 'boxes.txt'

# Settings constants
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
NUMBER_OF_MARBLES_IN_A_BAG = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ Bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

class Gift():
    """
    Gift of a large marble and a bag of marbles - Don't change

    Parameters:
        large_marble (string): The name of the large marble for this gift.
        marbles (Bag): A completed bag of small marbles for this gift.
    """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'

class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self,sleepTime,sendPipe,quantity):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.sendPipe = sendPipe
        self.quantity = quantity

        self.sleepTime = sleepTime
        

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        for _ in range(self.quantity):
            marble = random.choice(self.colors)
            # print(f"Creator sending: {marble}")
            self.sendPipe.send(marble)
            time.sleep(self.sleepTime)
        # print("Creator sending termination signal")
        self.sendPipe.send(None)


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, when there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self,receivePipe,sendPipe,sleepTime):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.receivePipe = receivePipe
        self.sendPipe = sendPipe
        self.sleepTime = sleepTime

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''

        while True:
            temp = Bag()
            while temp.get_size() < 8:
                marble = self.receivePipe.recv()
                # print(f'Received {marble}')
                if marble is None:
                    self.sendPipe.send(None)
                    return
                temp.add(marble)
                time.sleep(self.sleepTime)
            # print(f'sending baggy {temp}')
            self.sendPipe.send(temp)
        



class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Big Joe', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self,receivePipe,sendPipe,sleepTime):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.receivePipe = receivePipe
        self.sendPipe = sendPipe
        self.sleepTime = sleepTime

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while True:
            marbleBag = self.receivePipe.recv()
            if marbleBag is None:
                self.sendPipe.send(None)
                return
            bigMarble = random.choice(self.marble_names)
            assembledGift = Gift(bigMarble,marbleBag)
            self.sendPipe.send(assembledGift)
            time.sleep(self.sleepTime)
        


class Wrapper(mp.Process):
    """ Takes created gifts and "wraps" them by placing them in the boxes file. """
    def __init__(self,receivePipe,giftCount,filename,sleepTime):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.receivePipe = receivePipe
        self.giftCount = giftCount
        self.filename = filename
        self.sleepTime = sleepTime

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        with open(self.filename, 'a') as file:
            while True:
                giftBox = self.receivePipe.recv()
                if giftBox is None:
                    return
                file.write(f'Created - {datetime.now().time()}: {giftBox}\n')
                self.giftCount.value += 1
                time.sleep(self.sleepTime)


def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count     = {settings[MARBLE_COUNT]}')
    log.write(f'Marble delay     = {settings[CREATOR_DELAY]}')
    log.write(f'Marbles in a bag = {settings[NUMBER_OF_MARBLES_IN_A_BAG]}') 
    log.write(f'Bagger delay     = {settings[BAGGER_DELAY]}')
    log.write(f'Assembler delay  = {settings[ASSEMBLER_DELAY]}')
    log.write(f'Wrapper delay    = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    creator_sender, bagger_receiver = mp.Pipe()
    bagger_sender, assembler_receiver = mp.Pipe()
    assembler_sender, wrapper_receiver = mp.Pipe()

    # TODO create variable to be used to count the number of gifts
    giftCount = mp.Value("i", 0)

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)
    creator = Marble_Creator(settings[CREATOR_DELAY],creator_sender,settings[MARBLE_COUNT])
    # mp.Process(target=Marble_Creator,args=(CREATOR_DELAY,creator_parent,MARBLE_COUNT))
    bagger = Bagger(bagger_receiver,bagger_sender,settings[BAGGER_DELAY])
    # mp.Process(target=Bagger,args=(bagger_parent,assembler_receiver))
    assembler = Assembler(assembler_receiver,assembler_sender,settings[ASSEMBLER_DELAY])
    
    wrapper = Wrapper(wrapper_receiver,giftCount,BOXES_FILENAME,settings[WRAPPER_DELAY])

    log.write('Starting the processes')
    # TODO add code here
    creator.start()
    bagger.start()
    assembler.start()
    wrapper.start()

    log.write('Waiting for processes to finish')
    # TODO add code here
    creator.join()
    bagger.join()
    assembler.join()
    wrapper.join()


    display_final_boxes(BOXES_FILENAME, log)
    
    # TODO Log the number of gifts created.
    log.write(f'Total gifts: {giftCount.value}')


    log.stop_timer(f'Total time')




if __name__ == '__main__':
    main()
