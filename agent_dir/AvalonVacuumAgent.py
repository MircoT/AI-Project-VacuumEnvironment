from . agents import *
from random import randint


class AvalonVacuumAgentClass(Agent):

    def __init__(self, noCleans=10):
        Agent.__init__(self)
        self.img = 'agent_v5.png'
        self.actions = ['GoEast', 'GoWest', 'GoNorth', 'GoSouth']
        self.coord = (0, 0)
        self.visited = [(0, 0)]
        self.walls = []
        self.curr = 'GoEast'
        self.maxNoCleans = noCleans
        self.currNoCleans = 0
        self.consecNoCleans = 0

        def findCoord(coord, move):
            if move == 0:
                return (coord[0] + 1, coord[1])
            elif move == 1:
                return (coord[0] - 1, coord[1])
            elif move == 2:
                return (coord[0], coord[1] + 1)
            elif move == 3:
                return (coord[0], coord[1] - 1)

        def nextMove():
            index = randint(0, 3)
            if findCoord(self.coord, index) not in self.walls and findCoord(self.coord, index) not in self.visited:
                return self.actions[index]
            index += 1
            if index > 3:
                index = 0
            if findCoord(self.coord, index) not in self.walls and findCoord(self.coord, index) not in self.visited:
                return self.actions[index]
            index += 1
            if index > 3:
                index = 0
            if findCoord(self.coord, index) not in self.walls and findCoord(self.coord, index) not in self.visited:
                return self.actions[index]
            index += 1
            if index > 3:
                index = 0
            if findCoord(self.coord, index) not in self.walls and findCoord(self.coord, index) not in self.visited:
                return self.actions[index]
            index += 1
            if index > 3:
                index = 0
            if findCoord(self.coord, index) not in self.walls:
                return self.actions[index]
            index += 1
            if index > 3:
                index = 0
            if findCoord(self.coord, index) not in self.walls:
                return self.actions[index]
            index += 1
            if index > 3:
                index = 0
            if findCoord(self.coord, index) not in self.walls:
                return self.actions[index]
            index += 1
            if index > 3:
                index = 0
            if findCoord(self.coord, index) not in self.walls:
                return self.actions[index]

        def program(status, bump, neighbors)):
            if self.curr != 'NoOp':
                if bump == 'Bump':
                    if self.curr == 'GoEast':
                        self.walls.append((self.coord[0] + 1, self.coord[1]))
                    elif self.curr == 'GoWest':
                        self.walls.append((self.coord[0] - 1, self.coord[1]))
                    elif self.curr == 'GoNorth':
                        self.walls.append((self.coord[0], self.coord[1] + 1))
                    elif self.curr == 'GoSouth':
                        self.walls.append((self.coord[0], self.coord[1] - 1))
                    self.curr = nextMove()
                    return self.curr
                if status == 'Dirty':
                    self.currNoCleans -= 2
                    self.consecNoCleans = 0
                    return 'Suck'
                else:
                    self.consecNoCleans += 1
                    self.currNoCleans += 1
                    if self.maxNoCleans > 0 and self.currNoCleans > self.maxNoCleans:
                        self.curr = 'NoOp'
                        return self.curr
                    else:
                        if self.curr == 'GoEast':
                            self.coord = (self.coord[0] + 1, self.coord[1])
                        elif self.curr == 'GoWest':
                            self.coord = (self.coord[0] - 1, self.coord[1])
                        elif self.curr == 'GoNorth':
                            self.coord = (self.coord[0], self.coord[1] + 1)
                        elif self.curr == 'GoSouth':
                            self.coord = (self.coord[0], self.coord[1] - 1)
                        self.visited.append(self.coord)
                        self.curr = nextMove()
                    return self.curr
            else:
                return self.curr
        self.program = program
