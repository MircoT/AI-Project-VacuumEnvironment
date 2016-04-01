from . agents import *


class ExampleClass(Agent):

    def __init__(self, x=2, y=2):
        Agent.__init__(self)

        ##
        # Personalize the identifier of this class.
        # Will be used instead of the class name
        # in neighbours info
        self.name = 'ExampleAgent'

        def program(status, bump, neighbors):
            """Main function of the Agent.

            Params:
                status (string): 'Dirty' or 'Clean'
                bump (string): 'Bump' or 'None'
                neighbors (list of tuples): [
                        ( (agent_id, agent_type), (r_x, r_y) ),
                        ...,
                        ...
                    ]

            Returns:
                 (string): one of these commands:
                            - 'Suck'
                            - 'GoNorth'
                            - 'GoSouth'
                            - 'GoWest'
                            - 'GoEast'
                            - 'NoOp' or 'Noop'

            """
            print(self.id)
            print(status, bump, neighbors)

            ##
            # Check positions of neighbors
            for (agent_id, agent_class), pos in neighbors:
                if agent_id != self.id:
                    print(pos)

            ##
            # Go near first neighbor
            a_near = min([((agent_id, agent_class), pos)
                        for (agent_id, agent_class), pos in neighbors
                        if agent_id != self.id],
                        key=lambda obj: obj[1]  # select position as filter
                      )

            (agent_id, agent_class), pos = a_near

            if pos[0] < 0:
                return 'GoWest'
            elif pos[0] > 0:
                return 'GoEast'
            elif pos[1] < 0:
                return 'GoSouth'
            elif pos[1] > 0:
                return 'GoNorth'

            return 'NoOp'


        self.program = program
