"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: <your name>

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  

- Do not use try...except statements

- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can NOT use sleep() statements.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List(), Barrier() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable from the buffer>, end=', ', flush=True)

Add any comments for me:

"""

import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2

WRITE_INDEX = BUFFER_SIZE + 0
READ_INDEX = BUFFER_SIZE + 1
NEXT_NUM_INDEX = BUFFER_SIZE + 2
FINISHED_INDEX = BUFFER_SIZE + 3

def returnIncrement(val):
    return (val + 1) % BUFFER_SIZE

def writer(sharedList,empty_spaces,full_spaces,lock,id):
    while True:
        empty_spaces.acquire()
        # print(f'{sharedList}')
        with lock:
            if sharedList[NEXT_NUM_INDEX] > sharedList[FINISHED_INDEX]: # checks if writers are finished, ends
                if (id == 1):
                    sharedList[sharedList[READ_INDEX]] = None # Signal to readers to stop
                    for i in range(WRITERS): full_spaces.release()
                return
            sharedList[sharedList[WRITE_INDEX]] = sharedList[NEXT_NUM_INDEX]
            sharedList[NEXT_NUM_INDEX] += 1
            sharedList[WRITE_INDEX] = returnIncrement(sharedList[WRITE_INDEX])
        full_spaces.release()

def reader(sharedList,empty_spaces,full_spaces,lock,id):
    while True:
        full_spaces.acquire()
        with lock:
            if sharedList[sharedList[READ_INDEX]] == None:
                print(f'Reader {id} shutting down')
                if id == 1:
                    for i in range(READERS): empty_spaces.release()
                return
            readVal = sharedList[sharedList[READ_INDEX]]
            print(readVal, end=', ', flush=True)
            sharedList[READ_INDEX] = returnIncrement(sharedList[READ_INDEX])

        empty_spaces.release()

def main():

    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(1000, 10000)

    smm = SharedMemoryManager()
    smm.start()

    # TODO - Create a ShareableList to be used between the processes
    sharedList = smm.ShareableList([0]*BUFFER_SIZE + [0, 0, 1, items_to_send])

    empty_spaces = mp.Semaphore(BUFFER_SIZE)
    full_spaces = mp.Semaphore(0)
    lock = mp.Lock()

    writerProcesses = [mp.Process(target=writer,args=(sharedList,empty_spaces,full_spaces,lock,id)) for id in range(WRITERS)]
    readerProcesses = [mp.Process(target=reader,args=(sharedList,empty_spaces,full_spaces,lock,i)) for i in range(READERS)]

    for i in writerProcesses:
        i.start()
    for i in readerProcesses:
        i.start()

    for i in writerProcesses:
        i.join()
    for i in readerProcesses:
        i.join()

    #      - The buffer should be size 10 PLUS at least three other
    #        values (ie., [0] * (BUFFER_SIZE + 3)).  The extra values
    #        are used for the head and tail for the circular buffer.
    #        The another value is the current number that the writers
    #        need to send over the buffer.  This last value is shared
    #        between the writers.
    #        You can add another value to the shared list to keep
    #        track of the number of values received by the readers.
    #        (ie., [0] * (BUFFER_SIZE + 4))

    # TODO - Create any lock(s) or semaphore(s) that you feel you need

    # TODO - create reader and writer processes

    # TODO - Start the processes and wait for them to finish

    print(f'{items_to_send} values sent')

    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    # print(f'{<your variable>} values received')

    smm.shutdown()


if __name__ == '__main__':
    main()
