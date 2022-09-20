from typing import List
from enum import Enum, auto
from random import *
import pygame as pg
from math import sqrt
import random
#  Program to simulate segregation.
#  See : http:#nifty.stanford.edu/2014/mccown-schelling-model-segregation/
#

# Enumeration type for the Actors
class Actor(Enum):
    BLUE = auto()
    RED = auto()
    NONE = auto()  # NONE used for empty locations


# Enumeration type for the state of an Actor
class State(Enum):
    UNSATISFIED = auto()
    SATISFIED = auto()
    NA = auto()  # Not applicable (NA), used for NONEs


World = List[List[Actor]]  # Type alias


SIZE = 2000


def neighbours():
    pg.init()
    model = NeighborsModel(SIZE)
    _view = NeighboursView(model)
    #for event in pg.event.get():
     #   if event.key == pg.K_SPACE:

    model.run()

def create_flat_list(size):
    all_red = [Actor.RED] * int(size * NeighborsModel.DIST[0])
    all_blue = [Actor.BLUE] * int(size * NeighborsModel.DIST[1])
    all_none = [Actor.NONE] * int(size * NeighborsModel.DIST[2])
    flat_list_actors = all_none + all_red + all_blue
    shuffle(flat_list_actors)
    return flat_list_actors


class NeighborsModel:

    # Tune these numbers to test different distributions or update speeds
    SIDE = 0
    FRAME_RATE = 20            # Increase number to speed simulation up
    DIST = [0.35, 0.35, 0.3]  # % of RED, BLUE, and NONE
    THRESHOLD = 0.5            # % of surrounding neighbours that should be like me for satisfaction

    # ########### These following two methods are what you're supposed to implement  ###########
    # In this method you should generate a new world
    # using randomization according to the given arguments.
    @staticmethod
    def __create_world(size) -> World:
        flat_list_actors = create_flat_list(size)
        NeighborsModel.SIDE = int(sqrt(size))
        brave_new_world = []
        brave_new_world = NeighborsModel.create_new_matrix(flat_list_actors)
        print(len(brave_new_world))
        # TODO Create and populate world according to NeighborsModel.DIST distribution parameters
        return brave_new_world

    @staticmethod
    def create_new_matrix( flat_list_actors):
        new_matrix = [flat_list_actors[row_count * NeighborsModel.SIDE:(row_count + 1) * NeighborsModel.SIDE] for row_count in range(NeighborsModel.SIDE)]
        return new_matrix

    # This is the method called by the timer to update the world
    # (i.e move unsatisfied) each "frame".
    def __update_world(self):
        self.generate_new_world()
        # TODO Update logical state of world based on NeighborsModel.THRESHOLD satisfaction parameter
        pass
    def generate_new_world(self):
        for row_num in range(self.SIDE):
            new_row_list =[]
            for col_num in range(self.SIDE):
                update_actor_place = self.actor_action(row_num, col_num)

    def actor_action(self, row_num, col_num):
        actor_color = self.world[row_num][col_num]
        check_actor_neighbours = self.neighbourhood_check(row_num, col_num)

    def neighbourhood_check(self, row_num, col_num):
        #for event in pg.event.get():
         #   if event.type == pg.KEYDOWN:
                #if event.key == pg.K_SPACE:
        start_row_num, end_row_num = (max(0, row_num - 1), min(self.SIDE, row_num + 2))
        start_col_num, end_col_num = (max(0, col_num - 1), min(self.SIDE, col_num + 2))
        none_list_coordinates = []
        nr_of_blue = 0
        nr_of_red = 0
        nr_of_none = 0
        for i in range(start_row_num,end_row_num):
            for j in range(start_col_num, end_col_num):
                if not (i == row_num and j == col_num):
                    if self.world[i][j] == Actor.RED:
                        nr_of_red += 1
                    elif self.world[i][j] == Actor.BLUE:
                        nr_of_blue += 1
                    elif self.world[i][j] == Actor.NONE:
                        nr_of_none += 1
                    none_list_coordinates.append([i,j])
                self.update_actor(nr_of_blue, nr_of_red, i, j)
        #self.world = self.world2
        #print(self.world2)
        #print(self.world[16][16])
    def satisfiedred(self,nr_of_blue,nr_of_red):
        blank = (nr_of_blue + nr_of_red)
        if blank == 0:
            blank = 1
        satisfied = 1 - (nr_of_blue / blank)
        return satisfied
    def satisfiedblue(self,nr_of_blue,nr_of_red):
        blank = (nr_of_blue + nr_of_red)
        if blank == 0:
            blank = 1
        satisfied = 1 - (nr_of_red / blank)
        return satisfied

    def update_actor(self, nr_of_blue, nr_of_red, i, j):
        satisfied = self.satisfiedred(nr_of_blue,nr_of_red)

        if self.world[i][j] == Actor.RED and satisfied < NeighborsModel.THRESHOLD:
            posx = random.randint(0,(len(self.world)-1))
            posy = random.randint(0,(len(self.world)-1))

            while self.world[posx][posy] != Actor.NONE:
                posx = random.randint(0,(len(self.world)-1))
                posy = random.randint(0,(len(self.world)-1))
            self.world[posx][posy] = Actor.RED
            self.world[i][j] = Actor.NONE

        satisfied = self.satisfiedblue(nr_of_blue,nr_of_red)

        if self.world[i][j] == Actor.BLUE and satisfied < NeighborsModel.THRESHOLD:
            posx = random.randint(0,(len(self.world)-1))
            posy = random.randint(0,(len(self.world)-1))

            while self.world[posx][posy] != Actor.NONE: #and newmatrix[posx][posy]!=0:
                posx = random.randint(0,(len(self.world)-1))
                posy = random.randint(0,(len(self.world)-1))
            self.world[posx][posy] = Actor.BLUE
            self.world[i][j] = Actor.NONE

    # ########### the rest of this class is already defined, to handle the simulation clock  ###########
    def __init__(self, size):
        self.world: World = self.__create_world(size)
        #self.world2: World = self.__create_world2(size)
        #print(self.world2)
        self.observers = []  # for enabling discoupled updating of the view, ignore

    def run(self):
        clock = pg.time.Clock()
        running = True
        while running:
            running = self.__on_clock_tick(clock)
        # stop running
        print("Goodbye!")
        pg.quit()

    def __on_clock_tick(self, clock):
        clock.tick(self.FRAME_RATE)  # update no faster than FRAME_RATE times per second
        self.__update_and_notify()
        return self.__check_for_exit()

    # What to do each frame
    def __update_and_notify(self):
        self.__update_world()
        self.__notify_all()

    @staticmethod
    def __check_for_exit() -> bool:
        keep_going = True
        for event in pg.event.get():
            # Did the user click the window close button?
            if event.type == pg.QUIT:
                keep_going = False
        return keep_going

    # Use an Observer pattern for views
    def add_observer(self, observer):
        self.observers.append(observer)

    def __notify_all(self):
        for observer in self.observers:
            observer.on_world_update()


# ---------------- Helper methods ---------------------

# Check if inside world
def is_valid_location(size: int, row: int, col: int):
    return 0 <= row < size and 0 <= col < size


# ------- Testing -------------------------------------

# Here you run your tests i.e. call your logic methods
# to see that they really work
def test():
    # A small hard coded world for testing
    test_world = [
        [Actor.RED, Actor.RED, Actor.NONE],
        [Actor.NONE, Actor.BLUE, Actor.NONE],
        [Actor.RED, Actor.NONE, Actor.BLUE]
    ]

    th = 0.5  # Simpler threshold used for testing

    size = len(test_world)
    print(is_valid_location(size, 0, 0))
    print(not is_valid_location(size, -1, 0))
    print(not is_valid_location(size, 0, 3))
    print(is_valid_location(size, 2, 2))

    # TODO More tests

    exit(0)


# Helper method for testing
def count(a_list, to_find):
    the_count = 0
    for a in a_list:
        if a == to_find:
            the_count += 1
    return the_count


# ###########  NOTHING to do below this row, it's pygame display stuff  ###########
# ... but by all means have a look at it, it's fun!
class NeighboursView:
    # static class variables
    WIDTH = 400   # Size for window
    HEIGHT = 400
    MARGIN = 50

    WHITE = (255, 255, 255)
    RED   = (255,   0,   0)
    BLUE  = (  0,   0, 255)

    # Instance methods

    def __init__(self, model: NeighborsModel):
        pg.init()  # initialize pygame, in case not already done
        self.dot_size = self.__calculate_dot_size(len(model.world))
        self.screen = pg.display.set_mode([self.WIDTH, self.HEIGHT])
        self.model = model
        self.model.add_observer(self)

    def render_world(self):
        # # Render the state of the world to the screen
        self.__draw_background()
        self.__draw_all_actors()
        self.__update_screen()

    # Needed for observer pattern
    # What do we do every time we're told the model had been updated?
    def on_world_update(self):
        self.render_world()

    # private helper methods
    def __calculate_dot_size(self, size):
        return max((self.WIDTH - 2 * self.MARGIN) / size, 2)

    @staticmethod
    def __update_screen():
        pg.display.flip()

    def __draw_background(self):
        self.screen.fill(NeighboursView.WHITE)

    def __draw_all_actors(self):
        for row in range(len(self.model.world)):
            for col in range(len(self.model.world[row])):
                self.__draw_actor_at(col, row)

    def __draw_actor_at(self, col, row):
        color = self.__get_color(self.model.world[row][col])
        xy = self.__calculate_coordinates(col, row)
        pg.draw.circle(self.screen, color, xy, self.dot_size / 2)

    # This method showcases how to nicely emulate 'switch'-statements in python
    @staticmethod
    def __get_color(actor):
        return {
            Actor.RED: NeighboursView.RED,
            Actor.BLUE: NeighboursView.BLUE
        }.get(actor, NeighboursView.WHITE)

    def __calculate_coordinates(self, col, row):
        x = self.__calculate_coordinate(col)
        y = self.__calculate_coordinate(row)
        return x, y

    def __calculate_coordinate(self, offset):
        x: float = self.dot_size * offset + self.MARGIN
        return x


if __name__ == "__main__":
    neighbours()