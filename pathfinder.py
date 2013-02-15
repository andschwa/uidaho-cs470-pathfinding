#!/usr/bin/env python3

import argparse
import sys


class Input(object):
    """ Class object to parse input."""
    def __init__(self, filename='map.txt'):
        self._filename = filename
        self._size = ()
        self._start = ()
        self._goal = ()
        self._graph = ()
        self._costs = dict(zip(['R', 'f', 'F', 'h', 'r', 'M', 'W'],
                [1, 2, 4, 5, 7, 10, False]))

    def filename(self): return self._filename
    def width(self): return self._size[0]
    def height(self): return self._size[1]
    def start(self): return self._start
    def goal(self): return self._goal
    def graph(self): return self._graph
    def costs(self): return self._costs

    def _read_map(self, contents):
        """ Makes a tuple of tuple map from contents."""
        input_map = []
        for i in range(0, self.height()):
            input_map.append(tuple(list(contents[i])[:self.width()]))
        return tuple(input_map)

    def _read_contents(self):
        """ Opens map file and grabs size, start, goal, and map."""
        with open(self.filename(), 'r') as f:
            contents = f.readlines()

        self._size = tuple([int(i) for i in contents[0].split()])
        self._start = tuple([int(i) for i in contents[1].split()])
        self._goal = tuple([int(i) for i in contents[2].split()])
        self._graph = self._read_map(contents[3:])


class Search(Input):
    """ Class object to find path using assorted search methods."""
    def __init__(self, options, name=None):
        super().__init__(options.input_map)
        super()._read_contents()

        self._options = options
        self._name = name

        self._open = []
        self._closed = set()
        self._path = {}

    def options(self): return self._options
    def name(self): return self._name
    def count(self): return len(self.closed())

    def open(self): return self._open
    def closed(self): return self._closed
    def goal_test(self, state): return state == self.goal()

    def add_fringe(self, state):
        self._fringe.append(state)

    def add_closed(self, state):
        self._closed.append(state)

    def is_not_explored(self, state):
        return (is state not in self.fringe() and
                is state not in self.closed())

    def record_path(self, parent, state):
        self._path[parent] = state

    def state_cost(self, state):
        x, y = state
        return self.costs()[self.graph()[y][x]]

    def sort_fringe(self):
        self._fringe.sort(lambda a, b: cmp(self.state_cost(a), self.state_cost(b)))

    def _is_valid(self, state):
        """ Test if node is valid: i.e. real, on map, not explored, not in fringe, and not impassable water."""
        x, y = state
        if (x >= 0 and
            y >= 0 and
            x < self.width() and
            y < self.height() and
            self.graph()[y][x] != 'W'):
            return True
        else:
            return False

    def expand(self, state):
        """ Returns valid N, E, S, W coordinates as list."""
        result = []
        x, y = state
        neighbors = (
                    (x, y-1),
                    (x, y+1),
                    (x+1, y),
                    (x-1, y))
        for neighbor in neighbors:
            if self._is_valid(neighbor):
                result.append(neighbor)
        return result

    def breadth_first(self):
        def get_next(self):
            return self._fringe.pop(0)

        self.add_fringe(self.start())
        while self.fringe():
            parent = self.get_next()
            if self.goal_test(parent):
                return parent
            for child in self.expand(parent):
                if self.is_not_explored(child):
                    self.record_path(parent, child)
                    self.add_fringe(state)
            self.add_closed(parent)
        return None

    def uniform_cost_search(self):
        def get_next(self):
            return self._fringe.pop(0)

        self.add_fringe(self.start())
        while self.fringe():
            parent = self.get_next()
            if self.goal_test(parent):
                return parent
            for child in self.expand(parent):
                if self.is_not_explored(child):
                    self.record_path(parent, child)
                    self.add_fringe(state)
                    self.sort_fringe()
            self.add_closed(parent)
        return None


    def finish(self):
        """ Prints maps and resets lists."""
        self._print_explored()
        self._print_path()

    def _safe_filename(self, suffix):
        if self.name():
            return '_'.join((self.name(), suffix))
        else:
            return suffix

    def _print_explored(self):
        """ Prints an ASCII map of explored nodes."""
        filename = self._safe_filename(self.options().explored)
        with open(filename, 'w') as f:
            for y in range(0, self.height()):
                for x in range(0, self.width()):
                    if (x, y) == self.start():
                        f.write('@')
                    elif (x, y) == self.goal():
                        f.write('$')
                    elif (x, y) in self.path():
                        f.write('*')
                    elif (x, y) in self.closed():
                        f.write('#')
                    else:
                        f.write(self.graph()[y][x])
                f.write('\n')

    def _print_path(self):
        """ Prints an ASCII map of the found path from start to goal."""
        filename = self._safe_filename(self.options().path)
        with open(filename, 'w') as f:
            for y in range(0, self.height()):
                for x in range(0, self.width()):
                    if (x, y) == self.start():
                        f.write('@')
                    elif (x, y) == self.goal():
                        f.write('$')
                    elif (x, y) in self.path():
                        f.write('*')
                    else:
                        f.write(self.graph()[y][x])
                f.write('\n')


def parser():
    """ This is the option parser."""
    # TODO: Add type of search option
    parser = argparse.ArgumentParser(description='Find a path.')
    parser.add_argument('--map', dest='input_map', default='map.txt',
            help='Path to input map file.')
    parser.add_argument('--path', default='path.txt',
            help='Path to output map file of found path.')
    parser.add_argument('--explored', default='explored.txt',
            help='Path to output map file of all explored options.')
    return parser


def main():
    # Parse arguments and store in Args
    options = parser().parse_args()
    # Create Search object from Map

    # Execute search and print results
    searches = (
        Search(options, 'breadth_first'),
        Search(options, 'uniform_cost'),
        Search(options, 'iterative_deepening'),
        Search(options, 'a_star_1'),
        Search(options, 'a_star_2'))

    success_string = "{} method found path from ({}, {}) to ({}, {}),"
    success_string += " exploring {} nodes."
    fail_string = "{} method failed to find path."

    for search in searches:
        try:
            result = getattr(search, search.name())()
        except AttributeError as e:
            print("Could not find method '{}'".format(search.name()))
            raise
        else:
            if result is not None:
                search._path = search.get_path(result)
                print(success_string.format(
                    search.name(), search.start()[0], search.start()[1],
                    search.goal()[0], search.goal()[1], search.count()))
                search.finish()
            else:
                print(fail_string.format(search.name()))

if __name__ == "__main__":
   sys.exit(main())








