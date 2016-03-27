from . agents import *


class GBAgent24RClass(Agent):

    """An agent that performs a DFS exploration,
    guaranteed (hopefully) to clean everywhere.
    Actions array. Matches directions with the corresponding action.
    Directions are counted in counterclockwise order,
    starting from 0=East
    """

    def __init__(self, x=2, y=2):
        Agent.__init__(self)
        random.seed()
        self.actions = {}
        self.actions[0] = "GoEast"
        self.actions[1] = "GoNorth"
        self.actions[2] = "GoWest"
        self.actions[3] = "GoSouth"
        self.actions[4] = "NoOp"
        self.position = (1, 1)
        self.envMap = {}
        self.envMap[self.position] = ([1, 1, 1, 1], 4)
        self.heading = 0  # Default heading:east
        # Default action for the starting point: NoOp. Useful for termination.
        self.curr = 'NoOp'

        def insert_location(location, bump, parent=-1):
            """Inserts location into map.
            -1 as parent means that location contains a wall"""
            if bump == 'Bump':
                self.envMap[location] = ([0, 0, 0, 0], -1)
                self.envMap[location] = ([0, 0, 0, 0], -1)
                test = tuple(map(sum, list(zip(list(location), [1, 0]))))
                if test in self.envMap:
                    self.envMap[test][0][2] = 0
                test = tuple(map(sum, list(zip(list(location), [0, 1]))))
                if test in self.envMap:
                    self.envMap[test][0][3] = 0
                test = tuple(map(sum, list(zip(list(location), [-1, 0]))))
                if test in self.envMap:
                    self.envMap[test][0][0] = 0
                test = tuple(map(sum, list(zip(list(location), [0, -1]))))
                if test in self.envMap:
                    self.envMap[test][0][1] = 0
            else:
                self.envMap[location] = ([1, 1, 1, 1], parent)

        def calculate_position():
            """Calculates new position from actual position and heading"""
            # If we headed east, X+=1
            if self.heading == 0:
                return (self.position[0] + 1, self.position[1])
            # If we headed north, Y-=1
            elif self.heading == 1:
                return (self.position[0], self.position[1] + 1)
            # If we headed west, X-=1
            elif self.heading == 2:
                return (self.position[0] - 1, self.position[1])
            # If we headed south, Y+=1
            elif self.heading == 3:
                return (self.position[0], self.position[1] - 1)

        def program(xxx_todo_changeme):
            """The actual agent"""
            (status, bump) = xxx_todo_changeme
            if bump == 'Bump':
                if self.curr == "NoOp":
                    return self.curr
                insert_location(calculate_position(), bump)
                # Set last direction to 0 (cannot go in that direction)
                self.envMap[self.position][0][self.heading] = 0
                # Try all the 4 directions starting from the local node.
                for i in range(0, 4):
                    if (self.envMap[self.position][0][(self.heading + i) % 4]) == 1:
                        self.heading = (self.heading + i) % 4
                        self.curr = self.actions[self.heading]
                        self.envMap[self.position][0][self.heading] = 0
                        return self.curr

                # If this branch is executed, we are backtracking.
                self.heading = self.envMap[self.position][1]
                self.curr = self.actions[self.envMap[self.position][1]]
                return self.curr
            else:
                # Location updating: we moved
                # from a position to another one.
                if self.curr == "GoEast" or self.curr == "GoNorth" or self.curr == "GoWest" or self.curr == "GoSouth":
                    self.position = calculate_position()
                # Location insertion into map if it's the first time we enter
                # it
                if self.position not in self.envMap:
                    insert_location(self.position, bump,
                                    (self.heading + 2) % 4)
                    #test = tuple(map(sum, zip(list(self.position), [1, 0])))
                    test = tuple(map(sum, list(zip(list(self.position), [1, 0]))))
                    if test in self.envMap:
                        self.envMap[self.position][0][0] = 0
                        self.envMap[test][0][2] = 0
                    test = tuple(map(sum, list(zip(list(self.position), [0, 1]))))
                    if test in self.envMap:
                        self.envMap[self.position][0][1] = 0
                        self.envMap[test][0][3] = 0
                    test = tuple(map(sum, list(zip(list(self.position), [-1, 0]))))
                    if test in self.envMap:
                        self.envMap[self.position][0][2] = 0
                        self.envMap[test][0][0] = 0
                    test = tuple(map(sum, list(zip(list(self.position), [0, -1]))))
                    if test in self.envMap:
                        self.envMap[self.position][0][3] = 0
                        self.envMap[test][0][1] = 0
                # End of location insertion
                if status == 'Dirty':
                    self.curr = 'Suck'
                    return self.curr
                # If current location is Clean either we go in an unexplored
                # direction, or we backtrack.
                if status == 'Clean':
                    j = 0
                    while j < 6:
                        for i in range(0, 4):
                            if j < 5:
                                self.heading = self.heading + \
                                    random.randint(0, 1)
                            if self.envMap[self.position][0][(self.heading + i) % 4] == 1:
                                self.heading = (self.heading + i) % 4
                                self.curr = self.actions[self.heading]
                                self.envMap[self.position][0][self.heading] = 0
                                return self.curr
                        j = j + 1
                    # If this branch is executed, we are backtracking.
                    self.curr = self.actions[self.envMap[self.position][1]]
                    self.heading = self.envMap[self.position][1]
                    return self.curr
        self.program = program
