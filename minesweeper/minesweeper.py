import itertools
import random
from collections.abc import Iterable

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.mark_mine(cell)


    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.mark_safe(cell)

    def analyze_knowledge(self, new_sentence):
        new_sentence_copy = new_sentence.cells.copy()
        for cell in new_sentence_copy:

            if cell in self.safes:
                new_sentence.mark_safe(cell)

        for cell in new_sentence_copy:
            if cell in self.mines:
                new_sentence.mark_mine(cell)


        if isinstance(new_sentence.known_safes(), Iterable):
            for cell in new_sentence.known_safes():
                self.mark_safe(cell)


        if isinstance(new_sentence.known_mines(), Iterable):
            for cell in new_sentence.known_mines():
                self.mark_mine(cell)

        if not new_sentence in self.knowledge:
            self.knowledge.append(new_sentence)

            for sentence in self.knowledge:
                if sentence.cells != new_sentence.cells:
                    new_sentence_copy = new_sentence.cells.copy
                    sentence_copy = sentence.cells.copy()

                    for cell in sentence_copy:
                        if cell in self.safes:
                            sentence.mark_safe(cell)

                    for cell in sentence_copy:
                        if cell in self.mines:
                            sentence.mark_mine(cell)



                    if new_sentence.cells.issubset(sentence.cells):

                        cells = new_sentence.cells.copy()
                        for cell in cells:
                            sentence.cells.remove(cell)
                        sentence.count = sentence.count - new_sentence.count
                    if sentence.cells.issubset(new_sentence.cells):
                        cells = sentence.cells.copy()
                        for cell in cells:
                            new_sentence.cells.remove(cell)

                        new_sentence.count = new_sentence.count - sentence.count

                    if isinstance(sentence.known_mines(), Iterable):
                        cells = sentence.known_mines().copy()
                        for cell in cells:
                            self.mark_mine(cell)

                    if isinstance(sentence.known_safes(), Iterable):
                        cells = sentence.known_safes().copy()
                        for cell in cells:
                            self.mark_safe(cell)

                    if isinstance(new_sentence.known_mines(), Iterable):
                        cells = new_sentence.known_mines().copy()
                        for cell in cells:
                            self.mark_mine(cell)

                    if isinstance(new_sentence.known_safes(), Iterable):
                        cells = new_sentence.known_safes().copy()
                        for cell in cells:
                            self.mark_safe(cell)

                self.analyze_knowledge(sentence)
                self.analyze_knowledge(new_sentence)




    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        nearby_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell or (i, j) in self.safes or i not in range(self.height) or j not in range(self.width):
                    continue
                else:
                    nearby_cells.add((i, j))
        new_sentence = Sentence(nearby_cells, count)

        self.analyze_knowledge(new_sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        for safe in self.safes:
            if safe not in self.moves_made:
                return safe
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i,j) not in self.mines:
                    return (i, j)
        return None
