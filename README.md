AI-Project-VacuumEnvironment
============================

An environment to test a vacuum agent, created for a college college project and based on a problem from "Artificial Intelligence: A Modern Approach" by Stuart Russell and Peter Norvig.

## Dependencies

You must have [kivy](http://kivy.org/#home) installed on your system.

* [Download Kivy](https://kivy.org/#download)
* [Install Kivy on Windows](https://kivy.org/docs/installation/installation-windows.html)
* [Install kivy on Mac](https://kivy.org/docs/installation/installation-osx.html)

## Run the application

If you have installed all the dependencies, you can run the program with:
```bash
# To open the GUI with max 2 Agent (old program)
python aima-ui-2a.py

# To open the GUI with 4 Agent
python aima-ui-4a.py
```

## Add an Agent

You can write your own agent and add it to the environment. The procedure is simply, you have to follow these steps:

* Create a file in `agent_dir`, for example named `MyNewAgent.py`
* Add a class named like the file and ended with `Class`. In this example will be `MyNewAgentClass`
* Your class have to inherit from `Agent` class
* Insert your class in the list of imported module in `agent_dir/__init__.py`

Below we have an example `MyAgent.py` with some useful details:

```python
from . agents import *


class MyNewAgentClass(Agent):

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
            ##
            # id is assigned by the environment
            # in aima-ui-4a
            print(self.id)
            print(status, bump, neighbors)

            return 'NoOp'


        self.program = program

```

## Contributing

Contributions are welcome, so please feel free to fix bugs, improve things, provide documentation. 
For anything submit a personal message or fork the project to make a pull request and so on... thanks!

## Notes

This library is under development, so there may be substantial changes and improvements in the near future.

This project is based on [aima-python](https://code.google.com/p/aima-python/) for a course of artificial intelligence. In particular, these modules have been modified to meet the new specifications:

* Environment
* Agent
* utils

## Contributors

In this section will be mentioned all the people who have contributed to the creation of this program (the list will be in alphabetic order):

* [Nrevo](https://github.com/Nrevo)  
* [quiuquio](https://github.com/quiuquio)

... toDo

## License

The MIT License (MIT)

Copyright (c) 2014 Mirco

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
