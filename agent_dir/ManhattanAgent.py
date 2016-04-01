from . agents import *


class ManhattanAgentClass(Agent):

    """OMG my agent."""

    def __init__(self):
        """Initialize the Agent."""
        Agent.__init__(self)
        self.img = 'agent_v4'
        self.dirs = {
            'N': 'GoNorth',
            'S': 'GoSouth',
            'E': 'GoEast',
            'W': 'GoWest'
        }
        self.moves = {
            'N': lambda tup: (tup[0] +1, tup[1]),
            'S': lambda tup: (tup[0] -1, tup[1]),
            'E': lambda tup: (tup[0], tup[1]+1),
            'W': lambda tup: (tup[0], tup[1]-1)
        }
        self.reversed = {
            'N': 'S',
            'S': 'N',
            'E': 'W',
            'W': 'E'
        }
        self.world = {
            (1, 1): ["N", "S", "E", "W"]
        }
        self.walls = []
        self.path = []
        self.cleaned = []
        self.curr_pos = (1, 1)
        self.target = (1, 1)
        self.last_move = None

        from random import choice

        def update_pos(bump):
            if bump != "Bump":
                if self.last_move is not None:
                    self.curr_pos = self.moves[self.last_move](self.curr_pos)
                    if self.curr_pos not in self.world:
                        self.world[self.curr_pos] = ["N", "S", "E", "W"]
            else:
                if self.last_move is not None:
                    if self.last_move in self.world[self.curr_pos]:
                        self.world[self.curr_pos].remove(self.last_move)
                if self.curr_pos not in self.walls:
                    self.walls.append(
                        self.moves[self.last_move](self.curr_pos))
                self.target = self.curr_pos

        def update_world():
            for pos in list(self.world.keys()):
                for dir_, fun in list(self.moves.items()):
                    # print("UPDATE", pos, fun(pos))
                    if (fun(pos) in self.cleaned or fun(pos) in self.walls)\
                       and dir_ in self.world[pos]:
                        self.world[pos].remove(dir_)
            for pos in list(self.world.keys()):
                for dir_, fun in list(self.moves.items()):
                    # print("UPDATE2", pos, fun(pos))
                    if fun(pos) in self.world and\
                       dir_ not in self.world[fun(pos)] and\
                       dir_ in self.world[pos]:
                        self.world[pos].remove(dir_)

        def get_candidates():
            man_w = lambda s_c, d_c: abs(
                s_c[0] - d_c[0]) + abs(s_c[1] - d_c[1])
            dist = 0
            candidates = list()
            min_w, max_w = min(self.world.keys()), max(self.world.keys())
            max_dist = max([abs(min_w[0] + max_w[0]), abs(min_w[1] + max_w[1])])
            while len(candidates) == 0 and dist < max_dist:
                candidates = [pos for pos,
                              act in list(self.world.items()) if len(act) != 0 and
                              man_w(self.curr_pos, pos) <= dist]
                dist += 1
            return candidates

        def search_target():
            if self.curr_pos == self.target:
                candidates = get_candidates()
                # print("LEN CAND", len(candidates))
                if len(candidates) != 0:
                    chosen = choice(candidates)
                    # print("CHOSEN", chosen)
                    self.target = self.moves[
                        choice(self.world[chosen])](chosen)
                else:
                    self.target = False

        def manhattan_weights():
            man_w = lambda s_c, d_c: abs(
                s_c[0] - d_c[0]) + abs(s_c[1] - d_c[1])
            results = dict()
            for dir_, fun in list(self.moves.items()):
                weight = man_w(self.curr_pos, fun(self.curr_pos))
                if dir_ in self.world[self.curr_pos]:
                    if weight in results:
                        results[weight].append(dir_)
                    else:
                        results[weight] = [dir_]
            if len(results) == 0:
                for dir_, fun in list(self.moves.items()):
                    weight = man_w(self.curr_pos, fun(self.curr_pos))
                    if weight in results:
                        results[weight].append(dir_)
                    else:
                        results[weight] = [dir_]
            return results

        def check_move(dir_):
            new_dir = self.moves[dir_](self.curr_pos)
            if new_dir not in self.path and new_dir not in self.walls:
                return True
            return False

        def new_move():
            weights = manhattan_weights()
            # print("WEIGHTS", weights)
            move = choice(weights[min(weights)])
            if check_move(move):
                self.last_move = move
                return move
            else:
                self.path = list()
                return new_move()

        def move_me():
            if self.target is False:
                return "NoOp"
            else:
                return new_move()

        def program(status, bump, *largs):
            """Program of the agent."""
            update_pos(bump)
            update_world()
            if status == "Dirty":
                self.last_move = None
                self.cleaned.append(self.curr_pos)
                return "Suck"
            elif status == "Clean":
                if self.curr_pos not in self.cleaned:
                    self.cleaned.append(self.curr_pos)
                if self.curr_pos not in self.world:
                    self.world[self.curr_pos] = ["N", "S", "E", "W"]
            search_target()

            # print("---------------------")
            # print("TARGET", self.target)
            # print("CANDIDATES", [(pos, act)
            #       for pos, act in self.world.items() if len(act) != 0])
            # print("WALLS", self.walls)
            # print("CLEANED", self.cleaned)
            # print("######################")

            result = move_me()
            return self.dirs[result] if result in self.dirs else result

        self.program = program