__author__ = 'Amin'

import sys
import math
import numpy as np
from enum import Enum


class Direction(Enum):
    up = 1
    down = 2
    left = 3
    right = 4
    up_right = 5
    up_left = 6
    down_left = 7
    down_right = 8

    @staticmethod
    def get_opposite(direction):
        if direction == Direction.up:
            return Direction.down
        elif direction == Direction.down:
            return Direction.up
        elif direction == Direction.right:
            return Direction.left
        elif direction == Direction.left:
            return Direction.right
        elif direction == Direction.up_right:
            return Direction.up_left
        elif direction == Direction.up_left:
            return Direction.up_right
        elif direction == Direction.down_right:
            return Direction.down_left
        elif direction == Direction.down_left:
            return Direction.down_right


class Movements(Enum):
    vertical = 1
    horizontal = 2
    mixed = 3

    @staticmethod
    def get_opposite(movement):
        if movement == Movements.vertical:
            return Movements.horizontal
        elif movement == Movements.horizontal:
            Movements.vertical
        else:
            return Movements.mixed


class Building:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.usable_x_min = 0
        self.usable_x_max = self.width

        self.usable_y_min = 0
        self.usable_y_max = self.height

        self.map = np.zeros((self.height, self.width))#, dtype=np.uint8)

    def update_map(self, batman, bomb_distance):

        if bomb_distance == "SAME":
            if batman.direction_current == Direction.down:
                distance_traveled = batman.y_current - batman.y_previous

                y_start = batman.y_previous + distance_traveled // 2
                y_end = batman.y_current - distance_traveled // 2 + 1

                self.map[self.usable_y_min:y_start, self.usable_x_min:self.usable_x_max] = -1
                self.usable_y_min = y_start
                #self.map[0:y_start, :] = -1
                self.map[y_end:self.usable_y_max, self.usable_x_min:self.usable_x_max] = -1
                self.usable_y_max = y_end
                #self.map[y_end:self.height, :] = -1

            elif batman.direction_current == Direction.up:
                distance_traveled = batman.y_previous - batman.y_current

                y_start = batman.y_current + distance_traveled // 2
                y_end = batman.y_previous - distance_traveled // 2 + 1

                self.map[self.usable_y_min:y_start, self.usable_x_min:self.usable_x_max] = -1
                self.usable_y_min = y_start
                #self.map[0:y_start, :] = -1
                self.map[y_end:self.usable_y_max, self.usable_x_min:self.usable_x_max] = -1
                self.usable_y_max = y_end
                #self.map[y_end:self.height, :] = -1

            elif batman.direction_current == Direction.left:
                distance_traveled = batman.x_previous - batman.x_current

                x_start = batman.x_current + distance_traveled // 2
                x_end = batman.x_previous - distance_traveled // 2 + 1

                self.map[self.usable_y_min:self.usable_y_max, self.usable_x_min:x_start] = -1
                self.usable_x_min = x_start
                #self.map[batman.y_current, 0:x_start] = -1
                self.map[self.usable_y_min:self.usable_y_max, x_end:self.usable_x_max] = -1
                self.usable_x_max = x_end
                #self.map[batman.y_current, x_end:self.width] = -1

            elif batman.direction_current == Direction.right:
                distance_traveled = batman.x_current - batman.x_previous

                x_start = batman.x_previous + distance_traveled // 2
                x_end = batman.x_current - distance_traveled // 2 + 1

                self.map[self.usable_y_min:self.usable_y_max, self.usable_x_min:x_start] = -1
                self.usable_x_min = x_start
                #self.map[batman.y_current, 0:x_start] = -1
                self.map[self.usable_y_min:self.usable_y_max, x_end:self.usable_x_max] = -1
                self.usable_x_max = x_end
                #self.map[batman.y_current, x_end:self.width] = -1

            else:
                # TODO: this is special case and can be treated accordingly
                # if last direction is one of up_right, up_left, down_right, down_left do not update the map
                pass

        elif bomb_dist == "WARMER":
            if batman.direction_current == Direction.down:
                distance_traveled = batman.y_current - batman.y_previous

                y_start = batman.y_previous + distance_traveled // 2 + 1

                self.map[self.usable_y_min:y_start, self.usable_x_min:self.usable_x_max] = -1
                self.usable_y_min = y_start
                #self.map[0:y_start, :] = -1

            elif batman.direction_current == Direction.up:
                distance_traveled = batman.y_previous - batman.y_current

                y_end = batman.y_previous - distance_traveled // 2

                self.map[y_end:self.usable_y_max, self.usable_x_min:self.usable_x_max] = -1
                self.usable_y_max = y_end
                #self.map[y_end:self.height, :] = -1

            elif batman.direction_current == Direction.left:
                distance_traveled = batman.x_previous - batman.x_current

                x_end = batman.x_previous - distance_traveled // 2

                self.map[self.usable_y_min:self.usable_y_max, x_end:self.usable_x_max] = -1
                self.usable_x_max = x_end
                #self.map[batman.y_current, x_end:self.width] = -1

            elif batman.direction_current == Direction.right:
                distance_traveled = batman.x_current - batman.x_previous

                x_start = batman.x_previous + distance_traveled // 2 + 1

                self.map[self.usable_y_min:self.usable_y_max, self.usable_x_min:x_start] = -1
                self.usable_x_min = x_start
                #self.map[batman.y_current, 0:x_start] = -1

            else:
                # if last direction is one of up_right, up_left, down_right, down_left do not update the map
                pass

        elif bomb_distance == "COLDER":
            if batman.direction_current == Direction.down:
                distance_traveled = batman.y_current - batman.y_previous

                y_end = batman.y_current - distance_traveled // 2

                self.map[y_end:self.usable_y_max, self.usable_x_min:self.usable_x_max] = -1
                self.usable_y_max = y_end
                #self.map[y_end:self.height, :] = -1

            elif batman.direction_current == Direction.up:
                distance_traveled = batman.y_previous - batman.y_current

                y_start = batman.y_current + distance_traveled // 2 + 1

                self.map[self.usable_y_min:y_start, self.usable_x_min:self.usable_x_max] = -1
                self.usable_y_min = y_start
                #self.map[0:y_start, :] = -1

            elif batman.direction_current == Direction.left:
                distance_traveled = batman.x_previous - batman.x_current

                x_start = batman.x_current + distance_traveled // 2 + 1

                self.map[self.usable_y_min:self.usable_y_max, self.usable_x_min:x_start] = -1
                self.usable_x_min = x_start
                #self.map[batman.y_current, 0:x_start] = -1

            elif batman.direction_current == Direction.right:
                distance_traveled = batman.x_current - batman.x_previous

                x_end = batman.x_current - distance_traveled // 2

                self.map[self.usable_y_min:self.usable_y_max, x_end:self.usable_x_max] = -1
                self.usable_x_max = x_end
                #self.map[batman.y_current, x_end:self.width] = -1

            else:
                # if last direction is one of up_right, up_left, down_right, down_left do not update the map
                pass
        else:   # UNKNOWN
            pass

        #print(self.map, file=sys.stderr)
        print("self.usable_x_min: " + str(self.usable_x_min), file=sys.stderr)
        print("self.usable_x_max: " + str(self.usable_x_max), file=sys.stderr)
        print("self.usable_y_min: " + str(self.usable_y_min), file=sys.stderr)
        print("self.usable_y_max: " + str(self.usable_y_max), file=sys.stderr)


    def __update_map_distance_closer(self, x_start, x_end, y_start, y_end, flag_closer, flag_further):
        # iterate over all the cells, calculate previous and current distance and mark those that are closer / further than in previous step
        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                if self.map[y][x] == 0:
                    # TODO: POSSIBLE IMPROVEMENTS:
                    # initial:
                    # distance_previous = math.sqrt(pow(batman.x_previous - x, 2) + pow(batman.y_previous - y, 2))
                    # distance_current = math.sqrt(pow(batman.x_current - x, 2) + pow(batman.y_current - y, 2))
                    # remove sqrt!
                    # distance_previous = pow(batman.x_previous - x, 2) + pow(batman.y_previous - y, 2)
                    # distance_current = pow(batman.x_current - x, 2) + pow(batman.y_current - y, 2)
                    # change pow to multiply
                    distance_previous = (batman.x_previous - x) * (batman.x_previous - x) + (batman.y_previous - y) * (batman.y_previous - y)
                    distance_current = (batman.x_current - x) * (batman.x_current - x) + (batman.y_current - y) * (batman.y_current - y)

                    if flag_closer and not flag_further:
                        print("Remove those that are closer", file=sys.stderr)
                        if distance_current < distance_previous:
                            self.map[y][x] = distance_current

                    if flag_further and not flag_closer:
                        print("Remove those that are further", file=sys.stderr)
                        if distance_current > distance_previous:
                            self.map[y][x] = distance_current

                    if flag_further and flag_closer:
                        print("ERROR!!!", file=sys.stderr)
                    if not flag_further and not flag_closer:
                        print("ERROR!!!", file=sys.stderr)

    def find_movements_based_on_distance(self, bat, bomb_distance):

        direction = batman.direction_current

        if bomb_distance == "WARMER" or bomb_distance == "SAME":
            # last time we moved in right direction
            if direction == Direction.up_right or direction == Direction.up_left:
                direction = Direction.up
            elif direction == Direction.down_right or direction == Direction.down_left:
                direction = Direction.down
            else:
                direction = bat.direction_current

        elif bomb_distance == "COLDER":
            if direction == Direction.up:
                direction = Direction.down_right
            elif direction == Direction.down:
                direction = Direction.up_left
            elif direction == Direction.up_right or direction == Direction.up_left:
                direction = Direction.up
            elif direction == Direction.down_right or direction == Direction.down_left:
                direction = Direction.down
            else:
                # if this happens it means we are just in last row available
                # so right -> left, left -> right
                direction = Direction.get_opposite(direction)

        print("First direction guess: " + str(direction), file=sys.stderr)

        if direction != Direction.up_right and direction != Direction.up_left and \
            direction != Direction.down_right and direction != Direction.down_left:

            free_cells_in_current_direction = self.__count_number_of_free_cells_in_that_direction(bat.x_current, bat.y_current, direction)
            free_cells_in_opposing_direction = self.__count_number_of_free_cells_in_that_direction(bat.x_current, bat.y_current, Direction.get_opposite(direction))

            print("Free cells in current direction: " + str(free_cells_in_current_direction), file=sys.stderr)
            print("Free cells in opposing direction: " + str(free_cells_in_opposing_direction), file=sys.stderr)

            if free_cells_in_opposing_direction > free_cells_in_current_direction:
                direction = Direction.get_opposite(direction)
                print("Change direction in work!", file=sys.stderr)

        else:
            # we are going up_right, down_left, etc.
            # check if we are at usable_x_ max or min
            # if not go to closer of the two (NOT IMPLEMENTED RIGHT NOW)
            if bat.x_current == self.usable_x_min:
                if direction == Direction.up_left:
                    direction = Direction.up_right
                elif direction == Direction.down_left:
                    direction = Direction.down_right
            elif bat.x_current == self.usable_x_max:
                if direction == Direction.up_right:
                    direction = Direction.up_left
                elif direction == Direction.down_right:
                    direction = Direction.down_left

        print("Second direction guess: " + str(direction), file=sys.stderr)

        # TODO: what to do with top_right, down_left, etc.?
        # check if move is possible
        if direction != Direction.up_right and direction != Direction.up_left and \
            direction != Direction.down_right and direction != Direction.down_left:
            if not self.__check_if_there_are_free_cells_in_that_direction(bat.x_current, batman.y_current, direction):
                if self.__check_if_there_are_free_cells_in_that_direction(bat.x_current, batman.y_current, Direction.up):
                    return Direction.up
                if self.__check_if_there_are_free_cells_in_that_direction(bat.x_current, batman.y_current, Direction.down):
                    return Direction.down
                if self.__check_if_there_are_free_cells_in_that_direction(bat.x_current, batman.y_current, Direction.right):
                    return Direction.right
                if self.__check_if_there_are_free_cells_in_that_direction(bat.x_current, batman.y_current, Direction.left):
                    return Direction.left

        print("Final direction guess: " + str(direction), file=sys.stderr)

        return direction

    def __count_number_of_free_cells_in_that_direction(self, current_x, current_y, direction):
        free_cells = 0
        if direction == Direction.up:
            # check column above
            print("Checking column above", file=sys.stderr)
            for y in range(self.usable_y_min, current_y):
                if self.map[y][current_x] == 0:
                    free_cells += 1
        elif direction == Direction.down:
            # check column below
            print("Checking column below", file=sys.stderr)
            for y in range(current_y+1, self.usable_y_max+1):
                if self.map[y][current_x] == 0:
                    free_cells += 1
        if direction == Direction.left:
            # check row on the left
            print("Checking row on the left", file=sys.stderr)
            for x in range(self.usable_x_min, current_x):
                if self.map[current_y][x] == 0:
                    free_cells += 1
        elif direction == Direction.right:
            # check column below
            print("Checking row on the right", file=sys.stderr)
            for x in range(current_x+1, self.usable_x_max+1):
                if self.map[current_y][x] == 0:
                    free_cells += 1

        return free_cells

    def __check_if_there_are_free_cells_in_that_direction(self, current_x, current_y, direction):
        if direction == Direction.up:
            # check column above
            print("Checking column above", file=sys.stderr)
            for y in range(0, current_y):
                if self.map[y][current_x] == 0:
                    return True
        elif direction == Direction.down:
            # check column below
            print("Checking column below", file=sys.stderr)
            for y in range(current_y+1, self.height):
                if self.map[y][current_x] == 0:
                    return True
        if direction == Direction.left:
            # check row on the left
            print("Checking row on the left", file=sys.stderr)
            for x in range(0, current_x):
                if self.map[current_y][x] == 0:
                    return True
        elif direction == Direction.right:
            # check column below
            print("Checking row on the right", file=sys.stderr)
            for x in range(current_x+1, self.width):
                if self.map[current_y][x] == 0:
                    return True
        return False

    # bomb_distance = UNKNOWN
    def find_movements_first_round(self, current_x, current_y):

        if current_y < (self.height // 2):
            direction = Direction.down
            new_position = self.height - current_y # self.height//2
        else:
            direction = Direction.up
            new_position = self.height - current_y # self.height//2

        return direction, new_position

    def check_if_only_one_column_left(self):
        usable_x_width = self.usable_x_max - self.usable_x_min

        if usable_x_width == 1:
            return True
        else:
            return False

    def check_if_only_one_row_left(self):
        usable_y_width = self.usable_y_max - self.usable_y_min

        if usable_y_width == 1:
            return True
        else:
            return False

    def check_if_only_one_cell_left(self):
        usable_x_width = self.usable_x_max - self.usable_x_min
        usable_y_width = self.usable_y_max - self.usable_y_min

        if usable_x_width == 1 and usable_y_width == 1:
            return True
        else:
            return False

    def find_next_position_new(self, current_x, current_y, movement):

        usable_y_midpoint = (self.usable_y_max + self.usable_y_min) // 2
        usable_x_midpoint = (self.usable_x_max + self.usable_x_min) // 2

        print("Midpoint x: " + str(usable_x_midpoint) + ", y: " + str(usable_y_midpoint), file=sys.stderr)

        if movement == Movements.vertical:
            if current_y < usable_y_midpoint:
                if current_y < self.usable_y_min:
                    new_y = self.usable_y_min
                else:
                    new_y = (self.usable_y_max - 1) - (current_y - self.usable_y_min)
            else:
                if current_y > self.usable_y_max:
                    new_y = self.usable_y_max - 1
                else:
                    new_y = max(self.usable_y_min + ((self.usable_y_max - 1) - current_y), self.usable_y_min)

            print("New y: " + str(new_y), file=sys.stderr)

            return current_x, new_y
        elif movement == Movements.horizontal:
            if current_x < usable_x_midpoint:
                new_x = (self.usable_x_max - 1) - (current_x - self.usable_x_min)
            else:
                new_x = self.usable_x_min + ((self.usable_x_max - 1) - current_x)

            print("New x: " + str(new_x), file=sys.stderr)

            return new_x, current_y
        else:
            return self.usable_x_max-1, self.usable_y_max-1

    def find_next_position(self, current_x, current_y, direction):

        if direction != Direction.up_right and direction != Direction.up_left and \
            direction != Direction.down_right and direction != Direction.down_left:

            available_points = []

            if direction == Direction.up:
                for y in range(0, current_y):
                    if self.map[y][current_x] == 0:
                        available_points.append(y)
            elif direction == Direction.down:
                for y in range(current_y+1, self.height):
                    if self.map[y][current_x] == 0:
                        available_points.append(y)
            elif direction == Direction.right:
                for x in range(current_x+1, self.width):
                    if self.map[current_y][x] == 0:
                        available_points.append(x)
            elif direction == Direction.left:
                for x in range(0, current_x):
                    if self.map[current_y][x] == 0:
                        available_points.append(x)

            #available_points.sort()
            next_position = sum(available_points) / len(available_points)

            #if next_position - int(next_position) > 0:
                #next_position += 1

            if direction == Direction.up:
                #pass
                #next_position = available_points[int(0.25*len(available_points))]
                next_position = min(available_points)
            elif direction == Direction.down:
                #pass
                #next_position = available_points[int(0.75*len(available_points))]
                next_position = max(available_points)
            elif direction == Direction.left:
                #pass
                #next_position = available_points[int(0.25*len(available_points))]
                next_position = min(available_points)
            elif direction == Direction.right:
                #pass
                #next_position = available_points[int(0.75*len(available_points))]
                next_position = max(available_points)


            return int(next_position), 0

        else:
            if direction == Direction.up_right:
                return self.usable_y_min, self.usable_x_max
            elif direction == Direction.up_left:
                return self.usable_y_min, self.usable_x_min
            elif direction == Direction.down_right:
                return self.usable_y_max, self.usable_x_max
            elif direction == Direction.down_left:
                return self.usable_y_max, self.usable_x_min


class Batman:
    def __init__(self, x0, y0):
        self.x_current = x0
        self.y_current = y0

        self.x_previous = x0
        self.y_previous = y0

        self.movement = Movements.vertical

        self.direction_current = Direction.up
        self.direction_previous = Direction.up

        self.vertical_distance = "UNKNOWN"
        self.horizontal_distance = "UNKNOWN"

    def update_movement(self, current_distance):

        if current_distance != "UNKNOWN":
            if self.movement == Movements.vertical:
                self.vertical_distance = current_distance
                self.movement = Movements.horizontal
            elif self.movement == Movements.horizontal:
                self.horizontal_distance = current_distance
                if self.vertical_distance == "WARMER" and self.horizontal_distance == "WARMER":
                    self.movement = Movements.vertical
                else:
                    self.movement = Movements.mixed
            else:   # UNKNOWN
                self.movement = Movements.vertical
        else:
            pass

    def set_movement(self, new_movement):
        self.movement = new_movement

    def set_position(self, x, y):
        self.x_previous = self.x_current
        self.y_previous = self.y_current

        self.x_current = x
        self.y_current = y

        self.__update_direction()

    def __update_direction(self):
        # this could be decided based on self. movement, but this method is more general
        if self.x_current == self.x_previous:
            # vertical
            if self.y_current < self.y_previous:
                self.direction_current = Direction.up
            else:
                self.direction_current = Direction.down
        elif self.y_current == self.y_previous:
            # horizontal
            if self.x_current < self.x_previous:
                self.direction_current = Direction.left
            else:
                self.direction_current = Direction.right
        else:
            # one of mixed direction, does not matter which
            self.direction_current = Direction.up_right

    def update_based_on_direction2(self, direction, new_position_main, new_position_additional):
        self.x_previous = self.x_current
        self.y_previous = self.y_current

        self.direction_previous = self.direction_current
        self.direction_current = direction

        if direction == Direction.up:
            self.y_current = new_position_main
        elif direction == Direction.down:
            self.y_current = new_position_main
        elif direction == Direction.right:
            self.x_current = new_position_main
        elif direction == Direction.left:
            self.x_current = new_position_main
        elif direction == Direction.up_right or direction == Direction.up_left or \
            direction == Direction.down_right or direction == Direction.down_left:
            self.y_current = new_position_main
            self.x_current = new_position_additional
        else:
            print("ERROR!!! Batman can't update in that direction!", file=sys.stderr)

    def get_as_string(self):
        r = "Batman: \n"
        r += "x: " + str(self.x_current) + ", y: " + str(self.y_current) + "\n"
        r += "x_p: " + str(self.x_previous) + ", y_p: " + str(self.y_previous) + "\n"
        r += "dir: " + str(self.direction_current) + ", dir_p: " + str(self.direction_previous) + "\n"
        r += "dis_vertical: " + str(self.vertical_distance) + ", dis_horizontal: " + str(self.horizontal_distance) + "\n"
        r += "movement: " + str(self.movement)

        return r

if __name__ == '__main__':

    # w: width of the building.
    # h: height of the building.
    w, h = [int(i) for i in input().split()]

    print("w: " + str(w) + ", h: " + str(h), file=sys.stderr)

    n = int(input())  # maximum number of turns before game over.
    x0, y0 = [int(i) for i in input().split()]

    building = Building(w, h)
    batman = Batman(x0, y0)

    # game loop
    while 1:
        bomb_dist = input()  # Current distance to the bomb compared to previous distance (COLDER, WARMER, SAME or UNKNOWN)

        batman.update_movement(bomb_dist)

        print(batman.get_as_string(), file=sys.stderr)

        building.update_map(batman, bomb_dist)

        if building.check_if_only_one_cell_left():
            batman.set_position(building.usable_x_min, building.usable_y_min)
        else:
            if building.check_if_only_one_column_left():
                batman.set_movement(Movements.vertical)
            if building.check_if_only_one_row_left():
                batman.set_movement(Movements.horizontal)

            #print(building.map, file=sys.stderr)

            batman_new_x, batman_new_y = building.find_next_position_new(batman.x_current, batman.y_current, batman.movement)
            batman.set_position(batman_new_x, batman_new_y)

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)

        print(str(batman.x_current) + " " + str(batman.y_current))
