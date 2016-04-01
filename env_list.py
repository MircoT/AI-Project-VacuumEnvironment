from agent_dir.agents import *

__all__ = ["get_maps"]


class VacuumMap1(VacuumEnvironment):

    def __init__(self):
        super(VacuumMap1, self).__init__(8, 8)
        self.add_walls()
        self.dirty_all()
        self.start_from = (1, 2)


class VacuumMap2(VacuumEnvironment):

    def __init__(self):
        super(VacuumMap2, self).__init__(8, 8)
        self.add_walls()
        self.add_thing(Wall(), (3, 2))
        self.add_thing(Wall(), (3, 3))
        self.dirty_all()

class VacuumMap3(VacuumEnvironment):

    def __init__(self):
        super(VacuumMap3, self).__init__(4, 4)
        self.add_walls()
        self.add_thing(Wall(), (3, 1))
        self.add_thing(Wall(), (3, 2))
        self.dirty_all()


class VacuumMap4(VacuumEnvironment):

    def __init__(self):
        super(VacuumMap4, self).__init__(10, 10)
        self.add_walls()
        self.add_thing(Wall(), (5, 3))
        self.add_thing(Wall(), (5, 4))
        self.add_thing(Wall(), (5, 5))
        self.add_thing(Wall(), (5, 6))
        self.add_thing(Wall(), (5, 7))
        self.add_thing(Wall(), (6, 3))
        self.add_thing(Wall(), (7, 3))
        self.add_thing(Wall(), (8, 3))
        self.dirty_all()


class VacuumMap5(VacuumEnvironment):

    def __init__(self):
        super(VacuumMap5, self).__init__(10, 10)
        self.add_walls()
        self.add_thing(Wall(), (5, 3))
        self.add_thing(Wall(), (5, 4))
        self.add_thing(Wall(), (5, 5))
        self.add_thing(Wall(), (5, 6))
        self.add_thing(Wall(), (5, 7))
        self.add_thing(Wall(), (6, 3))
        self.add_thing(Wall(), (7, 3))
        self.add_thing(Wall(), (8, 3))
        self.add_thing(Wall(), (6, 7))
        self.add_thing(Wall(), (7, 7))
        self.add_thing(Wall(), (8, 7))
        self.dirty_all()


class VacuumMap6(VacuumEnvironment):

    def __init__(self):
        super(VacuumMap6, self).__init__(8, 8)
        self.init_env("""WWWWWWWW
WWWDDWWW
WDDDDDDW
WDCCDDDW
WWWDDWWW
WWWWWWWW
WWWWWWWW
WWWWWWWW""")
        self.start_from = (4, 4)


class VacuumMap7(VacuumEnvironment):

    def __init__(self):
        super(VacuumMap7, self).__init__(8, 8)
        self.add_walls()
        self.add_thing(Wall(), (1, 1))
        self.add_thing(Wall(), (1, 4))
        self.add_thing(Wall(), (1, 5))
        self.add_thing(Wall(), (1, 6))
        self.add_thing(Wall(), (1, 7))
        self.add_thing(Wall(), (2, 1))
        self.add_thing(Wall(), (2, 4))
        self.add_thing(Wall(), (2, 5))
        self.add_thing(Wall(), (2, 6))
        self.add_thing(Wall(), (2, 7))
        self.add_thing(Wall(), (4, 1))
        self.add_thing(Wall(), (4, 4))
        self.add_thing(Wall(), (4, 5))
        self.add_thing(Wall(), (4, 6))
        self.add_thing(Wall(), (4, 7))
        self.add_thing(Wall(), (5, 1))
        self.add_thing(Wall(), (5, 2))
        self.add_thing(Wall(), (5, 4))
        self.add_thing(Wall(), (5, 5))
        self.add_thing(Wall(), (5, 6))
        self.add_thing(Wall(), (5, 7))
        self.add_thing(Wall(), (6, 1))
        self.add_thing(Wall(), (6, 2))
        self.add_thing(Wall(), (6, 4))
        self.add_thing(Wall(), (6, 5))
        self.add_thing(Wall(), (6, 6))
        self.add_thing(Wall(), (6, 7))
        self.add_thing(Wall(), (7, 1))
        self.add_thing(Wall(), (7, 2))
        self.add_thing(Wall(), (7, 4))
        self.add_thing(Wall(), (7, 5))
        self.add_thing(Wall(), (7, 6))
        self.add_thing(Wall(), (7, 7))
        self.dirty_all()
        self.start_from = (3, 1)


class VacuumMap8(VacuumEnvironment):

    def __init__(self):
        super(VacuumMap8, self).__init__(8, 8)
        self.add_walls()
        self.add_thing(Wall(), (1, 4))
        self.add_thing(Wall(), (1, 5))
        self.add_thing(Wall(), (1, 6))
        self.add_thing(Wall(), (1, 7))
        self.add_thing(Wall(), (2, 1))
        self.add_thing(Wall(), (2, 4))
        self.add_thing(Wall(), (2, 5))
        self.add_thing(Wall(), (2, 6))
        self.add_thing(Wall(), (2, 7))
        self.add_thing(Wall(), (3, 1))
        self.add_thing(Wall(), (4, 1))
        self.add_thing(Wall(), (5, 1))
        self.add_thing(Wall(), (5, 2))
        self.add_thing(Wall(), (5, 3))
        self.add_thing(Wall(), (5, 4))
        self.add_thing(Wall(), (5, 5))
        self.dirty_all()


class VacuumMap9(VacuumEnvironment):

    def __init__(self):
        super(VacuumMap9, self).__init__(9, 9)
        self.add_walls()
        self.add_thing(Wall(), (1, 2))
        self.add_thing(Wall(), (1, 3))
        self.add_thing(Wall(), (1, 4))
        self.add_thing(Wall(), (1, 5))
        self.add_thing(Wall(), (1, 6))
        self.add_thing(Wall(), (2, 4))
        self.add_thing(Wall(), (2, 5))
        self.add_thing(Wall(), (2, 6))
        self.add_thing(Wall(), (3, 1))
        self.add_thing(Wall(), (3, 2))
        self.add_thing(Wall(), (3, 4))
        self.add_thing(Wall(), (3, 5))
        self.add_thing(Wall(), (3, 6))
        self.add_thing(Wall(), (4, 2))
        self.add_thing(Wall(), (4, 6))
        self.add_thing(Wall(), (5, 2))
        self.add_thing(Wall(), (5, 3))
        self.add_thing(Wall(), (5, 4))
        self.add_thing(Wall(), (5, 6))
        self.add_thing(Wall(), (6, 2))
        self.add_thing(Wall(), (6, 3))
        self.add_thing(Wall(), (7, 2))
        self.add_thing(Wall(), (7, 3))
        self.add_thing(Wall(), (7, 5))
        self.add_thing(Wall(), (7, 6))
        self.dirty_all()
        self.start_from = (2, 1)


def get_maps():
    return {
        "VacuumMap1": VacuumMap1,
        "VacuumMap2": VacuumMap2,
        "VacuumMap3": VacuumMap3,
        "VacuumMap4": VacuumMap4,
        "VacuumMap5": VacuumMap5,
        "VacuumMap6": VacuumMap6,
        "VacuumMap7": VacuumMap7,
        "VacuumMap8": VacuumMap8,
        "VacuumMap9": VacuumMap9
    }
