import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            for word in self.domains[var].copy():
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False

        for word_x in self.domains[x].copy():
            if len(self.domains[y]) == 0 or (len(self.domains[y]) == 1 and word_x in self.domains[y]):
                self.domains[x].remove(word_x)
                revised = True
        if self.domains[y] in self.crossword.neighbors(x):
            i, j = self.crossword.overlaps[self.domains[x], self.domains[y]]
            for word_x in self.domains[x].copy():
                no_word = True
                for word_y in self.domains[y]:
                    if word_x == word_y:
                        continue
                    if word_x[i] == word_y[j]:
                        no_word = False
                if no_word:
                    self.domains[x].remove(word_x)
                    revised = True

        # if self.domains[y] in self.crossword.neighbors(x):
        #     i, j = self.crossword.overlaps[self.domains[x], self.domains[y]]

        return revised


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        constraints = list()
        if arcs is None:
            arcs = self.domains

        for var1 in arcs:
            for var2 in arcs:
                if var1 == var2:
                    continue
                constraints.append((var1, var2))

        while len(constraints) > 0:
            X, Y = constraints.pop(0)
            if self.revise(X, Y):
                if X.length == 0:
                    return False
                for Z in arcs:
                    if Z == X or Z == Y:
                        continue
                    constraints.append((Z, X))
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.domains):
            return True
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        consistent = True
        for var in assignment:
            if var.length != len(assignment[var]):
                consistent = False
            for var2 in assignment:
                if var == var2:
                    continue
                if assignment[var] == assignment[var2]:
                    consistent = False
                if var2 in self.crossword.neighbors(var):
                    i, j = self.crossword.overlaps[var, var2]
                    if assignment[var][i] != assignment[var2][j]:
                        consistent = False
        return consistent



    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        n = list()

        for word in self.domains[var]:
            no = 0
            for var2 in self.domains:
                if var == var2 or var2 in assignment:
                    continue
                if word in self.domains[var2]:
                    no += 1
                if var2 in self.crossword.neighbors(var):
                    i, j = self.crossword.overlaps[var, var2]
                    for word2 in self.domains[var2]:
                        if word == word2:
                            continue
                        if word[i] != word2[j]:
                            no += 1
            n.append([word, no])
            n = sorted(n, key=lambda var: var[1])

        return list(row[0] for row in n)




    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_var = None
        min = float('inf')
        neighbors = -float('inf')
        for var in self.domains:
            if var in assignment:
                continue
            if len(self.domains[var]) < min:
                unassigned_var = var
                min = len(self.domains[var])
                neighbors = self.crossword.neighbors(var)
            if len(self.domains[var]) == min:
                if self.crossword.neighbors(var) > neighbors:
                    unassigned_var = var
                    min = len(self.domains[var])
                    neighbors = self.crossword.neighbors(var)
        return unassigned_var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)

        for word in self.order_domain_values(var, assignment):
            assignment[var] = word
            if self.consistent(assignment):
                inferences = self.ac3(assignment)


                result = self.backtrack(assignment)
                if result is not None:
                    return result
            del assignment[var]
        return None




def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
