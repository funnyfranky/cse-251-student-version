import multiprocessing as mp
import time


class Board:
    SIZE = 25

    directions = (
        (1, 0),   # E
        (1, 1),   # SE
        (0, 1),   # S
        (-1, 1),  # SW
        (-1, 0),  # W
        (-1, -1), # NW
        (0, -1),  # N
        (1, -1)   # NE
    )

    def __init__(self, lock, shared_highlighting):
        """ Create the instance and the board arrays """
        self.size = self.SIZE
        self.lock = lock
        self.shared_highlighting = shared_highlighting  # Shared highlighting array

        # Example predefined board
        self.board = [['L', 'S', 'O', 'D', 'A'] * 5] * self.SIZE  # Example board

    def highlight(self, row, col, on=True):
        """ Turn on/off highlighting for a letter (thread-safe) """
        with self.lock:  # Acquire lock to modify the shared array
            idx = row * self.SIZE + col
            self.shared_highlighting[idx] = on

    def get_size(self):
        """ Return the size of the board """
        return self.size

    def get_letter(self, x, y):
        """ Return the letter found at (x, y) """
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return ''
        return self.board[x][y]

    def display(self):
        """ Display the board with highlighting """
        with self.lock:  # Synchronize display
            print()
            for row in range(self.size):
                for col in range(self.size):
                    idx = row * self.SIZE + col
                    if self.shared_highlighting[idx]:
                        print(f'*{self.board[row][col]}* ', end='')
                    else:
                        print(f'{self.board[row][col]} ', end='')
                print()

    def _word_at_this_location(self, row, col, direction, word):
        """ Helper function: is the word found on the board at (x, y) in a direction """
        dir_x, dir_y = self.directions[direction]

        for letter in word:
            if self.get_letter(row, col) == letter:
                self.highlight(row, col)  # Thread-safe highlight
                row += dir_x
                col += dir_y
            else:
                return False
        return True

    def find_word(self, word):
        """ Find a word in the board """
        print(f'Finding {word}...')
        for row in range(self.size):
            for col in range(self.size):
                for d in range(0, 8):
                    if self._word_at_this_location(row, col, d, word):
                        return True
        return False


def worker(board, word):
    """ Worker function to find a word """
    if not board.find_word(word):
        print(f'Error: Could not find "{word}"')


def main():
    lock = mp.Lock()  # Create a multiprocessing lock
    size = Board.SIZE * Board.SIZE
    shared_highlighting = mp.Array('b', size)  # Shared boolean array (1D representation of 2D highlighting)

    # Initialize the board
    board = Board(lock, shared_highlighting)

    # Example word list
    words = ['BOOKMARK', 'SURNAME', 'RETHINKING']

    processes = []

    start = time.perf_counter()

    # Create and start processes
    for word in words:
        p = mp.Process(target=worker, args=(board, word))
        processes.append(p)
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

    total_time = time.perf_counter() - start

    board.display()  # Display the final board with highlighting
    print(f'Time to find words = {total_time}')


if __name__ == '__main__':
    main()
