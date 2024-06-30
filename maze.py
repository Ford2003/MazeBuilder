"""
This module handles the creation and generation of Mazes.
"""
from typing import List, Tuple, Dict
from random import randint, choice, shuffle
import matplotlib.pyplot as plt


class Cell:
    def __init__(self):
        self.walls: Dict[str, bool] = {"up": True, "down": True, "left": True, "right": True}
        self.visited: bool = False
        self.visited_from: Tuple[int, int] | None = None

    def __str__(self):
        return f"Cell(walls={self.walls}, visited={self.visited})"

    def __repr__(self):
        return f"Cell(walls={self.walls}, visited={self.visited})"


class Maze:
    def __init__(self, size: int):
        self.grid: List[List[Cell]] = [[Cell() for _ in range(size)] for _ in range(size)]
        self.size: int = size
        self.start: Tuple[int, int] | None = None

    def generate(self, method: str = 'depth-first') -> None:
        """
        Generate the maze using a randomised depth-first search algorithm.
        :param method: The method to use for generating the maze.
        :return: None
        """
        match method:
            case 'depth-first-1':
                self._depth_first_search_1()
            case 'depth-first-2':
                self._depth_first_search_2()
            case _:
                print(f'Invalid method {method}, using default.')
                self._depth_first_search_1()

    def _depth_first_search_1(self) -> None:
        self.start = self._initialise()

        stack = [self.start]
        # Utilise a set for seen cells to avoid visiting the same cell multiple times and for O(1) lookups.
        seen = set()
        while stack:
            current = stack.pop()
            self.grid[current[0]][current[1]].visited = True
            seen.add(current)
            neighbours = self._get_neighbouring_cells(current)
            unvisited = [neighbour for neighbour in neighbours if
                         not self.grid[neighbour[0]][neighbour[1]].visited and neighbour not in seen]
            for neighbour in unvisited:
                self.grid[neighbour[0]][neighbour[1]].visited_from = current
            seen.update(unvisited)
            # Randomise the neighbours so that the maze is more difficult.
            shuffle(unvisited)
            stack.extend(unvisited)
            # If we have unvisited neighbours, remove the wall between the current cell and the next cell.
            # This continues the current path.
            if unvisited:
                next_cell = stack[-1]
                self.remove_wall(current, next_cell)
            else:
                # We are at a dead-end, so we need to backtrack.
                # So to keep the maze connected we must remove the wall between the next cell and the cell it was
                # visited from.
                if stack:
                    next_cell = stack[-1]
                    self.remove_wall(self.grid[next_cell[0]][next_cell[1]].visited_from, next_cell)

    def _depth_first_search_2(self) -> None:
        # This version is slightly different to the first. It doesn't keep track of seen cells.
        # This causes a different style of maze to be generated, because duplicate cells can be added to the stack
        self.start = self._initialise()

        stack = [self.start]
        while stack:
            current = stack.pop()
            self.grid[current[0]][current[1]].visited = True
            neighbours = self._get_neighbouring_cells(current)
            unvisited = [neighbour for neighbour in neighbours if
                         not self.grid[neighbour[0]][neighbour[1]].visited]
            for neighbour in unvisited:
                self.grid[neighbour[0]][neighbour[1]].visited_from = current
            # Randomise the neighbours so that the maze is more difficult.
            shuffle(unvisited)
            stack.extend(unvisited)
            # If we have unvisited neighbours, remove the wall between the current cell and the next cell.
            # This continues the current path.
            if unvisited:
                next_cell = stack[-1]
                self.remove_wall(current, next_cell)
            else:
                # We are at a dead-end, so we need to backtrack.
                # So to keep the maze connected we must remove the wall between the next cell and the cell it was
                # visited from.
                if stack:
                    next_cell = stack[-1]
                    self.remove_wall(self.grid[next_cell[0]][next_cell[1]].visited_from, next_cell)

    def _get_neighbouring_cells(self, cell: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Given the coordinates of a cell, return the coordinates of its neighbours
        :param cell: The position of the cell.
        :return: A list of tuples containing the coordinates of the neighbouring cells.
        """
        neighbours = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x, y = cell
            x += dx
            y += dy
            if 0 <= x < self.size and 0 <= y < self.size:
                neighbours.append((x, y))
        return neighbours

    def _initialise(self) -> Tuple[int, int]:
        """
        Initialise the maze by choosing a random start cell on the edge of the maze, and an end cell on the opposite
        edge of the maze, to increase the difficulty of the maze.
        :return: The position of the start cell.
        """
        # Choose a random start cell for the maze on the edge.
        start = choice([(0, randint(0, self.size - 1)),                 # top edge
                        (randint(0, self.size - 1), 0),                 # left edge
                        (self.size - 1, randint(0, self.size - 1)),     # bottom edge
                        (randint(0, self.size - 1), self.size - 1)])    # right edge
        start_cell = self.grid[start[0]][start[1]]
        end = [0, 0]
        if start[0] == 0:
            start_cell.walls["up"] = False
            end[0] = self.size - 1
            end[1] = randint(0, self.size - 1)
            self.grid[end[0]][end[1]].walls["down"] = False
        elif start[0] == self.size - 1:
            start_cell.walls["down"] = False
            end[0] = 0
            end[1] = randint(0, self.size - 1)
            self.grid[end[0]][end[1]].walls["up"] = False
        elif start[1] == 0:
            start_cell.walls["left"] = False
            end[0] = randint(0, self.size - 1)
            end[1] = self.size - 1
            self.grid[end[0]][end[1]].walls["right"] = False
        else:
            start_cell.walls["right"] = False
            end[0] = randint(0, self.size - 1)
            end[1] = 0
            self.grid[end[0]][end[1]].walls["left"] = False
        return start

    def remove_wall(self, current_pos: Tuple[int, int], next_pos: Tuple[int, int]) -> None:
        """
        Remove the wall between 2 cells.
        :param current_pos: The position of the current cell.
        :param next_pos: The position of the next cell.
        """
        current_cell = self.grid[current_pos[0]][current_pos[1]]
        next_cell = self.grid[next_pos[0]][next_pos[1]]
        if next_pos[0] > current_pos[0]:    # Move down
            current_cell.walls["down"] = False
            next_cell.walls["up"] = False
        elif next_pos[0] < current_pos[0]:  # Move up
            current_cell.walls["up"] = False
            next_cell.walls["down"] = False
        elif next_pos[1] > current_pos[1]:  # Move right
            current_cell.walls["right"] = False
            next_cell.walls["left"] = False
        else:                               # Move left
            current_cell.walls["left"] = False
            next_cell.walls["right"] = False

    def display(self, debug=False) -> List[List[int]]:
        """
        Convert the grid into a pixel map 2D binary array. 1 = wall, 0 = path. For the purpose of displaying the maze.
        :param debug: Whether to display an image of the maze using matplotlib.
        :return: The pixel map of the maze.
        """
        display = [[1] * (2 * self.size + 1) for _ in range(2 * self.size + 1)]
        for row in range(2 * self.size + 1):
            for column in range(2 * self.size + 1):
                if row % 2 == 0 and row // 2 < self.size:
                    if column % 2 == 1:  # Looking above the cells
                        display[row][column] = self.grid[row // 2][(column - 1) // 2].walls["up"]
                if row // 2 == self.size:  # look at the bottom of the last row of cells
                    if column % 2 == 1:
                        display[row][column] = self.grid[(row // 2) - 1][(column - 1) // 2].walls["down"]
                if row % 2 == 1:
                    if column % 2 == 0 and column // 2 < self.size:  # look at the left of the cells
                        display[row][column] = self.grid[(row - 1) // 2][column // 2].walls["left"]
                    if column // 2 == self.size:  # look at the right of the last cells of the row
                        display[row][column] = self.grid[(row - 1) // 2][(column // 2) - 1].walls["right"]
                    if column % 2 == 1:  # This is a cell so shouldn't be coloured.
                        display[row][column] = 0
        if debug:
            plt.imshow(display, cmap='binary')
            plt.axis('off')
            plt.show()
        return display
