# MazeBuilder

A desktop app with a graphical interface for generating square mazes.

## Usage
<ins>EITHER:</ins>

Download app.exe and run it. This should work on Windows and Mac, but it is only tested on Windows. 

Click [here](https://github.com/Ford2003/MazeBuilder/releases/latest) for the latest release.

<ins>OR</ins>

Clone the repository:

`git clone https://github.com/Ford2003/MazeBuilder`

install the requirements:

`pip install -r requirements.txt`

Run app.py:

`python app.py`

## About the generator

The maze generator is created 100% out of python, and utilises a depth first search approach to create the maze.

Given a maze size, we create a 2D array of cells with all the walls around them. We pick a start and end cell and remove the appropriate walls, so the user can enter and exit the maze.

Now we use a stack to traverse the maze. For each cell we visit, we mark it as visited and add any unvisited neighbours of that cell onto the stack in a random order and remove the wall between the current cell and the next cell. If however a cell has no unvisited neighbours then we have reached a dead-end and must backtrack, in order to keep the maze connected, we remove the wall between the next cell and the cell that visited it. This creates a connected, random maze.

---

The GUI is created using PySide6. The maze is displayed by creating a QImage and setting each pixel colour from the output of the `Maze.display()` method, then converting it to a QPixmap and using that in a QLabel to show the image. The GUI also features a button to generate the mazes, a slider to determine maze size and radio buttons for the generation version.

---

I have 2 different generation methods, which both use the same algorithm with a small difference. Version 1 uses a set of seen cells, so when adding unvisited neighbours to the stack we also ensure they are unseen, this means each cell is eventually added to the stack exactly once, which ultimately just causes a stylistic variant which uses more memory, but slightly faster. Version 2 does not use a set of seen cells, so cells can be added to the stack multiple times and thus can be slightly slower than version 1.
