from . agents import *


class EconomicVacuumAgent_EVA01Class(Agent):

    def __init__(self, x=2, y=2):
        Agent.__init__(self)
        self.curr = 'GoEast'
        self.directions = ['GoEast', 'GoNorth', 'GoWest',  'GoSouth']
        self.movements = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.memory = {}
        self.x = 0
        self.y = 0
        self.expectedPosition = (self.x, self.y)
        self.position = (self.x, self.y)
        self.memory[self.position] = {0: 100, 1: 100, 2: 100, 3: 100}

        def nextCoord(position, action):
            if type(action) is str:
                action = self.directions.index(action)
            return vector_add(self.movements[action], position)

        def propagateWall(position):
            for i in range(4):
                pos = vector_add(self.movements[i], position)
                pos2 = vector_add(self.movements[(i + 1) % 4], pos)
                if pos in self.memory:
                    if (i + 2) % 4 in self.memory[pos]:
                        self.memory[pos].pop((i + 2) % 4)
                        #self.memory[pos][(i + 2) % 4] = 1
                else:
                    self.memory[pos] = {0: 100, 1: 100, 2: 100, 3: 100}
                    self.memory[pos].pop((i + 2) % 4)
            self.memory.pop(position)

        def propagateClean2(position):
            for i in range(4):
                pos = vector_add(self.movements[i], position)
                if pos in self.memory and (i + 2) % 4 in list(self.memory[pos].keys()):
                    self.memory[pos][(i + 2) % 4] /= 2
                elif position in self.memory and i in self.memory[position] and self.memory[position][i] != 0:
                    self.memory[pos] = {0: 100, 1: 100, 2: 100, 3: 100}
                    self.memory[pos][(i + 2) % 4] /= 2

        def keywithmaxval(d):
            v = list(d.values())
            k = list(d.keys())
            return k[v.index(max(v))]

        def mapDict(f, dictionary):
            return dict(
                [(k_v[0], f(k_v[1])) for k_v in iter(dictionary.items())]
            )

        def transDir(action):
            if type(action) is str:
                return self.directions.index(action)

        def decodeInstruction(instruction):
            if instruction == "NoOp":
                return instruction
            else:
                return self.directions[instruction]

        def updatePosition(bump):
            if bump != "Bump":
                self.position = self.expectedPosition

        def reduceMapSize():
            toPop = []
            for point in self.memory:
                eraseThis = True
                if len(self.memory[point]) < 4:
                    mapDict(lambda x: 100, self.memory[point])
                elif len(self.memory[point]) == 4:
                    if any([val for val in list(self.memory[point].values()) if val >= 100]):
                        surroudedByClean = False
                    else:
                        surroudedByClean = True
                    if surroudedByClean:
                        for i in range(4):
                            pos = vector_add(self.movements[i], point)
                            if pos in self.memory and len(self.memory[pos]) == 4:
                            # if pos in self.memory:
                                self.memory[pos][(i + 2) % 4] = 0
                            else:
                                eraseThis = False
                        if point != self.position and eraseThis:
                            toPop.append(point)
            return toPop

        def think3():
            if self.position in self.memory:
                toPop = reduceMapSize()
                for bad in toPop:
                    print("I'm breaking", bad)
                    self.memory.pop(bad)
                if any([val for val in list(self.memory[self.position].values()) if val != 0]):
                    retVal = keywithmaxval(self.memory[self.position])
                else:
                    return "NoOp"
                return retVal
            return "NoOp"

        def program(status, bump, *largs):
            if self.curr == "NoOp":
                return self.curr
            updatePosition(bump)
            if status == "Dirty":
                return "Suck"
            elif bump == "Bump":
                propagateWall(nextCoord(self.position, self.curr))
            elif status == "Clean":
                propagateClean2(self.position)
            instruction = think3()
            self.curr = decodeInstruction(instruction)
            if self.curr != "NoOp":
                self.expectedPosition = nextCoord(self.position, self.curr)
            return self.curr

        self.program = program
