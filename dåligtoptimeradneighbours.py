from importlib.metadata import DistributionFinder
from typing import List
from enum import Enum, auto
from random import *
import pygame as pg
from math import sqrt
import copy

#  Program to simulate segregation.
#  See : http:#nifty.stanford.edu/2014/mccown-schelling-model-segregation/
#

# Enumeration type for the Actors
class Actor(Enum):
    BLUE = auto()
    RED = auto()
    NONE = auto()  # NONE used for empty locations
    TEMPORARY = auto()


# Enumeration type for the state of an Actor
class State(Enum):
    UNSATISFIED = auto()
    SATISFIED = auto()
    NA = auto()  # Not applicable (NA), used for NONEs


World = List[List[Actor]]  # Type alias

SIZE = 90000


def neighbours():
    pg.init()
    model = NeighborsModel(SIZE)
    _view = NeighboursView(model)
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
    FRAME_RATE = 20  # Increase number to speed simulation up
    DIST = [0.25, 0.25, 0.5]  # % of RED, BLUE, and NONE
    THRESHOLD = 0.7  # % of surrounding neighbours that should be like me for satisfaction

    # ########### These following two methods are what you're supposed to implement  ###########
    # In this method you should generate a new world
    # using randomization according to the given arguments.
    @staticmethod
    def __create_world(size) -> World:
        flat_list_actors = create_flat_list(size)
        NeighborsModel.SIDE = int(sqrt(size))
        brave_new_world = NeighborsModel.create_new_matrix(flat_list_actors)
        # TODO Create and populate world according to NeighborsModel.DIST distribution parameters
        return brave_new_world

    @staticmethod
    def create_new_matrix(flat_list_actors):
        new_matrix = [flat_list_actors[row_count * NeighborsModel.SIDE:(row_count + 1) * NeighborsModel.SIDE] for
                      row_count in range(NeighborsModel.SIDE)]
        return new_matrix

    # This is the method called by the timer to update the world
    # (i.e move unsatisfied) each "frame".
    def __update_world(self):
        none_list_coordinates = []
        temporary_list: List[List[Actor]] = copy.deepcopy(self.world)
        unsatisfied: List[tuple[int, int]] = []
        for row_num in range(self.SIDE):
            for col_num in range(self.SIDE):
                if self.world[row_num][col_num] == Actor.NONE:
                    none_list_coordinates.append([row_num, col_num])
                unsatisfied = self.neighbourhood_check(row_num, col_num, unsatisfied)
        temporary_list = self.switch_pos(none_list_coordinates, unsatisfied, temporary_list)
        self.world: List[List[Actor]] = temporary_list



    #def generate_new_world(self):


    #def actor_action(self, row_num, col_num, none_list_coordinates):
     #   unsatisfied = self.neighbourhood_check(row_num, col_num,none_list_coordinates)
      #  return unsatisfied
    def neighbourhood_check(self, row_num, col_num, unsatisfied):
        start_row_num, end_row_num = (max(0, row_num - 1), min(self.SIDE, row_num + 2))
        start_col_num, end_col_num = (max(0, col_num - 1), min(self.SIDE, col_num + 2))
        nr_of_blue = 0
        nr_of_red = 0
        nr_of_none = 0
        for i in range(start_row_num, end_row_num):
            for j in range(start_col_num, end_col_num):
                if not (i == row_num and j == col_num):
                    if self.world[i][j] == Actor.RED:
                        nr_of_red += 1
                    elif self.world[i][j] == Actor.BLUE:
                        nr_of_blue += 1
                    elif self.world[i][j] == Actor.NONE:
                        nr_of_none += 1
        colortotal = 8 - nr_of_none
        if colortotal == 0:
            colortotal = 1
        if self.world[row_num][col_num] == Actor.RED:
            satisfiedrod = self.satisfiedred(nr_of_blue, colortotal)
            if satisfiedrod < self.THRESHOLD:
                unsatisfied.append((row_num, col_num))

        if self.world[row_num][col_num] == Actor.BLUE:
            satisfiedbla = self.satisfiedblue(nr_of_red, colortotal)
            if satisfiedbla < self.THRESHOLD:
                unsatisfied.append((row_num, col_num))
        return unsatisfied

    def satisfiedred(self, nr_of_blue, colortotal):

        sadneighbourpercentage = (nr_of_blue / colortotal)
        satisfiedred = 1 - sadneighbourpercentage
        return satisfiedred

    def satisfiedblue(self, nr_of_red, colortotal):

        sadneighbourpercentage = (nr_of_red / colortotal)
        satisfiedblue = 1 - sadneighbourpercentage
        return satisfiedblue

    def switch_pos(self, none_list_coordinates, unsatisfied,temporary_list):
        shuffle(none_list_coordinates)
        shuffle(unsatisfied)
        while len(none_list_coordinates) > 0 and len(unsatisfied) > 0:
            temporary_list[none_list_coordinates[0][0]][none_list_coordinates[0][1]] = self.world[unsatisfied[0][0]][
                unsatisfied[0][1]]
            temporary_list[unsatisfied[0][0]][unsatisfied[0][1]] = Actor.NONE
            none_list_coordinates.remove(none_list_coordinates[0])
            unsatisfied.remove(unsatisfied[0])
        return temporary_list
            # ########### the rest of this class is already defined, to handle the simulation clock  ###########

    def __init__(self, size):
        self.world: World = self.__create_world(size)
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
    WIDTH = 800  # Size for window
    HEIGHT = 800
    MARGIN = 50

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

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