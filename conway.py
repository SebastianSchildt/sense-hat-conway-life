from itertools import product
from random import choice,randrange
from time import sleep
from sense_hat import SenseHat

sense = SenseHat()

class GameOfLife(object):
    def __init__(self, width, height):
        self.size = (width, height)
	self.random_colour()
        self.random_world()

    def __str__(self):
        width, height = self.size
        return '\n'.join(
            ' '.join(
                self.draw_cell(x, y) for x in range(width)
            )
            for y in range(height)
        )

    def __iter__(self):
        return self

    def __next__(self):
        self.evolve_world()
        return self

    next = __next__

    def evolve_cell(self, cell):
        alive = cell in self.live_cells
        neighbours = self.count_neighbours(cell)
        return neighbours == 3 or (alive and neighbours == 2)

    def count_neighbours(self, cell):
        x, y = cell
        deltas = set(product([-1, 0, 1], repeat=2)) - set([(0, 0)])
        neighbours = ((x + dx, y + dy) for (dx, dy) in deltas)
        return sum(neighbour in self.live_cells for neighbour in neighbours)

    def evolve_world(self):
        width, height = self.size
        world = product(range(width), range(height))
        self.live_cells = {cell for cell in world if self.evolve_cell(cell)}

    def random_world(self):
        width, height = self.size
        world = product(range(width), range(height))
        self.live_cells = {cell for cell in world if choice([0, 1])}
	
    def random_colour(self):
	self.colour=(randrange(255), randrange(255), randrange(255))

    def draw_cell(self, x, y):
        cell = (x, y)
        return 'O' if cell in self.live_cells else ' '

    def get_cell_color(self, x, y):
        cell = (x, y)
        black = (0, 0, 0)
        return self.colour if cell in self.live_cells else black

    def update(self):
        width, height = self.size
        for x in range(width):
            for y in range(height):
                color = self.get_cell_color(x, y)
                sense.set_pixel(x, y, color)

    def count_cells(self):
	count=0
	width, height = self.size
	for x in range(width):
	    for y in range(height):
		if (x,y) in self.live_cells:
		    count=count+1
	return count

def main():
    game = GameOfLife(8, 8)
    oldcount=0
    boredom=0

    for i in game:
        game.update()
	newcount=game.count_cells()
        boredom+=0.01 # Get bored after 1000 generations, even if oscillatory steady state

        if newcount==oldcount: # Steady-state
	    boredom=boredom+1

	if newcount==0 or boredom>10:
	    sleep(2)
	    game.random_world()
	    game.random_colour()
	    boredom=0

        oldcount=newcount
	sleep(0.25)

if __name__ == '__main__':
    main()
