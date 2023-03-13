import random


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
        mine_cells = set()
        
        if self.count == len(self.cells) and self.count != 0:
            mine_cells = self.cells

        return mine_cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safe_cells = set()
        
        if self.count == 0:
            safe_cells = self.cells
        
        return safe_cells
        

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        
        if cell in self.cells:   
            self.count -= 1
            self.cells.remove(cell)
        
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
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)


    def get_cells_around(self, cell, count):
        """
        Returns all of the available correct fields around the cell
        """
        
        available_cells = set()
        row, column = cell
        
        for index_row in range(1,-2,-1):
            for index_cell in  range(1,-2,-1):
                current_row = row-index_row
                current_cell = column - index_cell

                if (current_row, current_cell) == cell:
                    continue

                if (current_row, current_cell) in self.safes:
                    continue

                if (current_row, current_cell) in self.mines:
                    count = count - 1
                    continue
                
                if (current_row >= 0 and current_row <= self.height - 1) and (current_cell >= 0 and current_cell <= self.width - 1):
                    available_cells.add((current_row, current_cell))
                    
        
        return (available_cells, count)
                    
    def learn(self):
        
        empty = Sentence(set(), 0)
        self.knowledge[:] = [x for x in self.knowledge if x != empty]   
        
        safes = set()
        mines = set()

        for sentence in self.knowledge:
            safes = safes.union(sentence.known_safes())
            mines = mines.union(sentence.known_mines())

        for first_sentence in self.knowledge:
            for second_sentence in self.knowledge:
                
                if first_sentence == second_sentence:
                    continue
                
                if first_sentence.count > 0 and first_sentence.cells == set():
                    raise ValueError
                
                if second_sentence.count > 0 and second_sentence.cells == set():
                    raise ValueError
                    
                if first_sentence.cells.issubset(second_sentence.cells):
                    new_sentence_cells = second_sentence.cells - first_sentence.cells
                    new_sentence_count = second_sentence.count - first_sentence.count

                    new_sentence = Sentence(new_sentence_cells, new_sentence_count)

                    if new_sentence not in self.knowledge:
                        self.knowledge.append(new_sentence)
                        self.learn()


    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
                
        (neighbor_cells, count) = self.get_cells_around(cell, count)
        new_sentence = Sentence(neighbor_cells, count)
        
        self.knowledge.append(new_sentence)
        
        if count == 0:
            for safe_cell in neighbor_cells:
                self.mark_safe(safe_cell)
                
        if count == len(neighbor_cells):
            for safe_cell in neighbor_cells:
                self.mark_mine(safe_cell)
            
        self.learn()      

            
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        
        safe_moves = self.safes - self.moves_made
        
        if(len(safe_moves) > 0):
            return random.choice(list(safe_moves))
        else:
            return None
       


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        moves = {}
        all_mines = 8

        number_mines_left = all_mines - len(self.mines)
        spaces_left = (self.height * self.width) - (len(self.moves_made) + len(self.mines))

        if spaces_left == 0:
            return None

        basic_prob = number_mines_left / spaces_left

        for i in range(0, self.height):
            for j in range(0, self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    moves[(i, j)] = basic_prob

        if moves and not self.knowledge:
            move = random.choice(list(moves.keys()))
            return move

        elif moves:
            for sentence in self.knowledge:
                num_cells = len(sentence.cells)
                count = sentence.count
                mine_probability = count / num_cells

                for cell in sentence.cells:
                    if moves[cell] < mine_probability:
                        moves[cell] = mine_probability

            move_list = [[x, moves[x]] for x in moves]
            move_list.sort(key=lambda x: x[1])
            best_prob = move_list[0][1]

            best_moves = [x for x in move_list if x[1] == best_prob]
            move = random.choice(best_moves)[0]

            return move