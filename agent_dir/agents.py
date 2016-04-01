"""Implement Agents and Environments (Chapters 1-2).

The class hierarchies are as follows:

Thing ## A physical object that can exist in an environment
    Agent
        Wumpus
    Dirt
    Wall
    ...

Environment ## An environment holds objects, runs simulations
    XYEnvironment
        VacuumEnvironment
        WumpusEnvironment

An agent program is a callable instance, taking percepts and choosing actions
    SimpleReflexAgentProgram
    ...

EnvGUI ## A window with a graphical representation of the Environment

EnvToolbar ## contains buttons for controlling EnvGUI

EnvCanvas ## Canvas to display the environment of an EnvGUI

"""

# TO DO:
# Implement grabbing correctly.
# When an object is grabbed, does it still have a location?
# What if it is released?
# What if the grabbed or the grabber is deleted?
# What if the grabber moves?
#
# Speed control in GUI does not have any effect -- fix it.

from utils import *
import random
import copy
import collections

#______________________________________________________________________________


class Thing(object):

    """This represents any physical object that can appear in an Environment.
    You subclass Thing to get the things you want.  Each thing can have a
    .__name__  slot (used for output only)."""

    def __repr__(self):
        return '<%s>' % getattr(self, '__name__', self.__class__.__name__)

    def is_alive(self):
        "Things that are 'alive' should return true."
        return hasattr(self, 'alive') and self.alive

    def show_state(self):
        "Display the agent's internal state.  Subclasses should override."
        print("I don't know how to show_state.")

    def display(self, canvas, x, y, width, height):
        # Do we need this?
        "Display an image of this Thing on the canvas."
        pass


class Agent(Thing):

    """An Agent is a subclass of Thing with one required slot,
    .program, which should hold a function that takes one argument, the
    percept, and returns an action. (What counts as a percept or action
    will depend on the specific environment in which the agent exists.)
    Note that 'program' is a slot, not a method.  If it were a method,
    then the program could 'cheat' and look at aspects of the agent.
    It's not supposed to do that: the program can only look at the
    percepts.  An agent program that needs a model of the world (and of
    the agent itself) will have to build and maintain its own model.
    There is an optional slot, .performance, which is a number giving
    the performance measure of the agent in its environment."""

    def __init__(self, program=None):
        self.alive = True
        self.bump = False
        self.img = None
        if program is None:
            def program(percept):
                return input('Percept=%s; action? ' % percept)
        assert isinstance(program, collections.Callable)
        self.program = program

    def can_grab(self, thing):
        """Returns True if this agent can grab this thing.
        Override for appropriate subclasses of Agent and Thing."""
        return False


def TraceAgent(agent):
    """Wrap the agent's program to print its input and output. This will let
    you see what the agent is doing in the environment."""
    old_program = agent.program

    def new_program(*percept):
        action = old_program(*percept)
        print('loc:%s: perf:%s %s percept:%s action:%s' % (agent.location, agent.performance, agent, percept, action))
        return action
    agent.program = new_program
    return agent

#______________________________________________________________________________


def TableDrivenAgentProgram(table):
    """This agent selects an action based on the percept sequence.
    It is practical only for tiny domains.
    To customize it, provide as table a dictionary of all
    {percept_sequence:action} pairs. [Fig. 2.7]"""
    percepts = []

    def program(percept):
        percepts.append(percept)
        action = table.get(tuple(percepts))
        return action
    return program


def RandomAgentProgram(actions):
    "An agent that chooses an action at random, ignoring all percepts."
    return lambda percept: random.choice(actions)

#______________________________________________________________________________


def SimpleReflexAgentProgram(rules, interpret_input):
    "This agent takes action based solely on the percept. [Fig. 2.10]"
    def program(percept):
        state = interpret_input(percept)
        rule = rule_match(state, rules)
        action = rule.action
        return action
    return program


def ModelBasedReflexAgentProgram(rules, update_state):
    "This agent takes action based on the percept and state. [Fig. 2.12]"
    def program(percept):
        program.state = update_state(program.state, program.action, percept)
        rule = rule_match(program.state, rules)
        action = rule.action
        return action
    program.state = program.action = None
    return program


def rule_match(state, rules):
    "Find the first rule that matches state."
    for rule in rules:
        if rule.matches(state):
            return rule

#______________________________________________________________________________

loc_A, loc_B = (0, 0), (1, 0)  # The two locations for the Vacuum world


def RandomVacuumAgent():
    "Randomly choose one of the actions from the vacuum environment."
    return Agent(RandomAgentProgram(['Right', 'Left', 'Suck', 'NoOp']))


def TableDrivenVacuumAgent():
    "[Fig. 2.3]"
    table = {((loc_A, 'Clean'),): 'Right',
             ((loc_A, 'Dirty'),): 'Suck',
             ((loc_B, 'Clean'),): 'Left',
             ((loc_B, 'Dirty'),): 'Suck',
             ((loc_A, 'Clean'), (loc_A, 'Clean')): 'Right',
             ((loc_A, 'Clean'), (loc_A, 'Dirty')): 'Suck',
             # ...
             ((loc_A, 'Clean'), (loc_A, 'Clean'), (loc_A, 'Clean')): 'Right',
             ((loc_A, 'Clean'), (loc_A, 'Clean'), (loc_A, 'Dirty')): 'Suck',
             # ...
             }
    return Agent(TableDrivenAgentProgram(table))


def ReflexVacuumAgent():
    "A reflex agent for the two-state vacuum environment. [Fig. 2.8]"
    def program(xxx_todo_changeme):
        (location, status) = xxx_todo_changeme
        if status == 'Dirty':
            return 'Suck'
        elif location == loc_A:
            return 'Right'
        elif location == loc_B:
            return 'Left'
    return Agent(program)


def ModelBasedVacuumAgent():
    "An agent that keeps track of what locations are clean or dirty."
    model = {loc_A: None, loc_B: None}

    def program(xxx_todo_changeme1):
        "Same as ReflexVacuumAgent, except if everything is clean, do NoOp."
        (location, status) = xxx_todo_changeme1
        model[location] = status  # Update the model here
        if model[loc_A] == model[loc_B] == 'Clean':
            return 'NoOp'
        elif status == 'Dirty':
            return 'Suck'
        elif location == loc_A:
            return 'Right'
        elif location == loc_B:
            return 'Left'
    return Agent(program)

#______________________________________________________________________________


class Environment(object):

    """Abstract class representing an Environment.  'Real' Environment classes
    inherit from this. Your Environment will typically need to implement:
        percept:           Define the percept that an agent sees.
        execute_action:    Define the effects of executing an action.
                           Also update the agent.performance slot.
    The environment keeps a list of .things and .agents (which is a subset
    of .things). Each agent has a .performance slot, initialized to 0.
    Each thing has a .location slot, even though some environments may not
    need this."""

    def __init__(self):
        self.things = []
        self.agents = []

    def thing_classes(self):
        return []  # List of classes that can go into environment

    def percept(self, agent):
        "Return the percept that the agent sees at this point. (Implement this.)"
        return NotImplementedError

    def execute_action(self, agent, action):
        "Change the world to reflect this action. (Implement this.)"
        return NotImplementedError

    def default_location(self, thing):
        "Default location to place a new thing with unspecified location."
        return None

    def exogenous_change(self):
        "If there is spontaneous change in the world, override this."
        pass

    def is_done(self):
        "By default, we're done when we can't find a live agent."
        return not any(agent.is_alive() for agent in self.agents)

    def step(self):
        """Run the environment for one time step. If the
        actions and exogenous changes are independent, this method will
        do.  If there are interactions between them, you'll need to
        override this method."""
        if not self.is_done():
            actions = [agent.program(*self.percept(agent))
                       for agent in self.agents]
            for (agent, action) in zip(self.agents, actions):
                self.execute_action(agent, action)
            self.exogenous_change()

    def run(self, steps=1000):
        "Run the Environment for given number of time steps."
        for step in range(steps):
            if self.is_done():
                return
            self.step()

    def list_things_at(self, location, tclass=Thing):
        "Return all things exactly at a given location."
        return [thing for thing in self.things
                if thing.location == location and isinstance(thing, tclass)]

    def some_things_at(self, location, tclass=Thing):
        """Return true if at least one of the things at location
        is an instance of class tclass (or a subclass)."""
        return self.list_things_at(location, tclass) != []

    def add_thing(self, thing, location=None):
        """Add a thing to the environment, setting its location. For
        convenience, if thing is an agent program we make a new agent
        for it. (Shouldn't need to override this."""
        if not isinstance(thing, Thing):
            thing = Agent(thing)
        assert thing not in self.things, "Don't add the same thing twice"
        thing.location = location or self.default_location(thing)
        self.things.append(thing)
        if isinstance(thing, Agent):
            thing.performance = 0
            self.agents.append(thing)

    def delete_thing(self, thing):
        """Remove a thing from the environment."""
        try:
            if thing.__class__.__name__ in REVERT:
                self.add_thing(
                    REVERT[thing.__class__.__name__](), thing.location)
            self.things.remove(thing)
        except ValueError as e:
            print(e)
            print("  in Environment delete_thing")
            print("  Thing to be removed: %s at %s" % (thing, thing.location))
            print("  from list: %s" % [(thing, thing.location)
                                       for thing in self.things])
        if thing in self.agents:
            self.agents.remove(thing)


class XYEnvironment(Environment):

    """This class is for environments on a 2D plane, with locations
    labelled by (x, y) points, either discrete or continuous.

    Agents perceive things within a radius.  Each agent in the
    environment has a .location slot which should be a location such
    as (0, 1), and a .holding slot, which should be a list of things
    that are held."""

    def __init__(self, width=10, height=10):
        super(XYEnvironment, self).__init__()
        update(self, width=width, height=height, observers=[])

    def things_near(self, location, radius=None):
        "Return all things within radius of location."
        if radius is None:
            radius = self.perceptible_distance
        radius2 = radius * radius
        return [thing for thing in self.things
                if distance2(location, thing.location) <= radius2]

    perceptible_distance = 1

    def percept(self, agent):
        "By default, agent perceives things within a default radius."
        return [self.thing_percept(thing, agent)
                for thing in self.things_near(agent.location)]

    def execute_action(self, agent, action):
        agent.bump = False
        if action == 'GoNorth':
            self.move_to(agent, vector_add((0, +1), agent.location))
        elif action == 'GoSouth':
            self.move_to(agent, vector_add((0, -1), agent.location))
        elif action == 'GoEast':
            self.move_to(agent, vector_add((+1, 0), agent.location))
        elif action == 'GoWest':
            self.move_to(agent, vector_add((-1, 0), agent.location))

    def thing_percept(self, thing, agent):  # ??? Should go to thing?
        "Return the percept for this thing."
        return thing.__class__.__name__

    def default_location(self, thing):
        return (random.choice(range(self.width)), random.choice(range(self.height)))

    def random_location(self):
        is_wall = True

        while is_wall:
            loc = (random.choice(range(self.width)), random.choice(range(self.height)))
            is_wall = False
            for thing in self.things_near(loc, 1):
                if isinstance(thing, Wall) and thing.location == loc:
                    is_wall = True
        return loc

    def move_to(self, thing, destination):
        "Move a thing to a new location."
        thing.bump = self.some_things_at(destination, Obstacle)
        if not thing.bump:
            thing.location = destination
            for o in self.observers:
                o.thing_moved(thing)

    def add_thing(self, thing, location=(1, 1)):
        super(XYEnvironment, self).add_thing(thing, location)
        thing.holding = []
        thing.held = None
        for obs in self.observers:
            obs.thing_added(thing)

    def delete_thing(self, thing):
        super(XYEnvironment, self).delete_thing(thing)
        # Any more to do?  Thing holding anything or being held?
        for obs in self.observers:
            obs.thing_deleted(thing)

    def init_env(self, string):
        objs = {
            "W": Wall,
            "D": Dirt,
            "C": Clean
        }
        s_x, s_y = 0, 0
        for line in string.splitlines():
            for char in list(line):
                self.add_thing(objs[char](), (s_x, s_y))
                s_x += 1
            s_y += 1
            s_x = 0

    def add_walls(self):
        "Put walls around the entire perimeter of the grid."
        for x in range(self.width + 1):
            self.add_thing(Wall(), (x, 0))
            self.add_thing(Wall(), (x, self.height))
        for y in range(self.height + 1):
            self.add_thing(Wall(), (0, y))
            self.add_thing(Wall(), (self.width, y))

    def add_observer(self, observer):
        """Adds an observer to the list of observers.
        An observer is typically an EnvGUI.

        Each observer is notified of changes in move_to and add_thing,
        by calling the observer's methods thing_moved(thing)
        and thing_added(thing, loc)."""
        self.observers.append(observer)

    def turn_heading(self, heading, inc):
        "Return the heading to the left (inc=+1) or right (inc=-1) of heading."
        return turn_heading(heading, inc)


def turn_heading(heading, inc,
                 headings=[(1, 0), (0, 1), (-1, 0), (0, -1)]):
    "Return the heading to the left (inc=+1) or right (inc=-1) in headings."
    return headings[(headings.index(heading) + inc) % len(headings)]


class Obstacle(Thing):

    """Something that can cause a bump, preventing an agent from
    moving into the same square it's in."""
    pass


class Wall(Obstacle):
    pass

#______________________________________________________________________________
# Vacuum environment


class Dirt(Thing):
    pass


class Clean(Thing):
    pass

REVERT = {
    "Dirt": Clean
}


class VacuumEnvironment(XYEnvironment):

    """The environment of [Ex. 2.12]. Agent perceives dirty or clean,
    and bump (into obstacle) or not; 2D discrete world of unknown size;
    performance measure is 100 for each dirt cleaned, and -1 for
    each turn taken."""

    def __init__(self, width=10, height=10):
        super(VacuumEnvironment, self).__init__(width, height)
        self.start_from = (1, 1)

    def thing_classes(self):
        return [Wall, Dirt, ReflexVacuumAgent, RandomVacuumAgent,
                TableDrivenVacuumAgent, ModelBasedVacuumAgent]

    def percept(self, agent):
        """The percept is a tuple of ('Dirty' or 'Clean', 'Bump' or 'None').
        Unlike the TrivialVacuumEnvironment, location is NOT perceived."""
        status = if_(self.some_things_at(agent.location, Dirt),
                     'Dirty', 'Clean')
        bump = if_(agent.bump, 'Bump', 'None')

        neighbors = []

        for cur_n_agent in [thing for thing in self.things
                            if isinstance(thing, Agent)]:
            loc = cur_n_agent.location
            agent_type = getattr(cur_n_agent, 'name',
                                 cur_n_agent.__class__.__name__)
            if getattr(cur_n_agent, 'id', None) is not None:
                id_ = ("{0}".format(cur_n_agent.id),
                       "{0}".format(agent_type)
                       )
            else:
                id_ = ("{0}".format(id(cur_n_agent)),
                       "{0}".format(agent_type)
                       )
            neighbors.append((
                id_,
                (loc[0]-agent.location[0],
                 loc[1]-agent.location[1]))
            )

        return status, bump, neighbors

    def execute_action(self, agent, action):
        if action == 'Suck':
            dirt_list = self.list_things_at(agent.location, Dirt)
            if dirt_list != []:
                dirt = dirt_list[0]
                agent.performance += 100
                self.delete_thing(dirt)
            else:
                agent.performance -= 20
        elif action != 'NoOp' and action != 'Noop':
            super(VacuumEnvironment, self).execute_action(agent, action)
            agent.performance -= 5

    def add_dirty(self, location):
        "Put Dirt in a given location of the grid."
        self.add_thing(Dirt(), location)

    def dirty_all(self):
        "Place Dirty Everywhere"
        for y in range(1, self.height):
            for x in range(1, self.width):
                something = False
                for thing in self.things:
                    if thing.location == (x, y):
                        something = True
                        break
                if not something:
                    self.add_dirty((x, y))


class TrivialVacuumEnvironment(Environment):

    """This environment has two locations, A and B. Each can be Dirty
    or Clean.  The agent perceives its location and the location's
    status. This serves as an example of how to implement a simple
    Environment."""

    def __init__(self):
        super(TrivialVacuumEnvironment, self).__init__()
        self.status = {loc_A: random.choice(['Clean', 'Dirty']),
                       loc_B: random.choice(['Clean', 'Dirty'])}

    def thing_classes(self):
        return [Wall, Dirt, ReflexVacuumAgent, RandomVacuumAgent,
                TableDrivenVacuumAgent, ModelBasedVacuumAgent]

    def percept(self, agent):
        "Returns the agent's location, and the location status (Dirty/Clean)."
        return (agent.location, self.status[agent.location])

    def execute_action(self, agent, action):
        """Change agent's location and/or location's status; track performance.
        Score 10 for each dirt cleaned; -1 for each move."""
        if action == 'Right':
            agent.location = loc_B
            agent.performance -= 1
        elif action == 'Left':
            agent.location = loc_A
            agent.performance -= 1
        elif action == 'Suck':
            if self.status[agent.location] == 'Dirty':
                agent.performance += 10
            self.status[agent.location] = 'Clean'

    def default_location(self, thing):
        "Agents start in either location at random."
        return random.choice([loc_A, loc_B])


class Gold(Thing):
    pass


class Pit(Thing):
    pass


class Arrow(Thing):
    pass


class Wumpus(Agent):
    pass


class Explorer(Agent):
    pass


class WumpusEnvironment(XYEnvironment):

    def __init__(self, width=10, height=10):
        super(WumpusEnvironment, self).__init__(width, height)
        self.add_walls()

    def thing_classes(self):
        return [Wall, Gold, Pit, Arrow, Wumpus, Explorer]

    # Needs a lot of work ...


#______________________________________________________________________________

def compare_agents(EnvFactory, AgentFactories, n=10, steps=1000):
    """See how well each of several agents do in n instances of an environment.
    Pass in a factory (constructor) for environments, and several for agents.
    Create n instances of the environment, and run each agent in copies of
    each one for steps. Return a list of (agent, average-score) tuples."""
    envs = [EnvFactory() for i in range(n)]
    return [(A, test_agent(A, steps, copy.deepcopy(envs)))
            for A in AgentFactories]


def test_agent(AgentFactory, steps, envs):
    "Return the mean score of running an agent in each of the envs, for steps"
    def score(env):
        agent = AgentFactory()
        env.add_thing(agent)
        env.run(steps)
        return agent.performance
    return mean(list(map(score, envs)))

#_________________________________________________________________________

__doc__ += """
>>> a = ReflexVacuumAgent()
>>> a.program((loc_A, 'Clean'))
'Right'
>>> a.program((loc_B, 'Clean'))
'Left'
>>> a.program((loc_A, 'Dirty'))
'Suck'
>>> a.program((loc_A, 'Dirty'))
'Suck'

>>> e = TrivialVacuumEnvironment()
>>> e.add_thing(ModelBasedVacuumAgent())
>>> e.run(5)

## Environments, and some agents, are randomized, so the best we can
## give is a range of expected scores.  If this test fails, it does
## not necessarily mean something is wrong.
>>> envs = [TrivialVacuumEnvironment() for i in range(100)]
>>> def testv(A): return test_agent(A, 4, copy.deepcopy(envs))
>>> 7 < testv(ModelBasedVacuumAgent) < 11
True
>>> 5 < testv(ReflexVacuumAgent) < 9
True
>>> 2 < testv(TableDrivenVacuumAgent) < 6
True
>>> 0.5 < testv(RandomVacuumAgent) < 3
True
"""
