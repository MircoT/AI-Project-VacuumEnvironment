'''
aima-ui project
=============

This is just a graphic user interface to test
agents for an AI college course.
'''

from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from functools import partial
from agents_dir.agents import *
import agents_list
import envs_list
from os import path

ALL_AGENTS = agents_list.load_agents()
ALL_MAPS = envs_list.ALL_MAPS


def check_img(img_name):
    """Check if the image is in img dir of the agents."""
    return path.isfile(path.join("agents_dir", path.join("img", img_name)))


def memoize(func):
    """Memoize decorator."""
    memo = {}

    def helper(*args):
        """Helper function for memoize paradigm."""
        if args not in memo:
            memo[args] = func(*args)
        return memo[args]
    return helper


@memoize
def gen_popup(type_, text, dismiss=True):
    """Generate a popup."""
    popup_layout = BoxLayout(orientation='vertical')
    content = Button(text='Dismiss', size_hint=(1, .3))
    popup_layout.add_widget(Label(text=text))
    popup = Popup(title=type_,
                  content=popup_layout)
    if dismiss:
        popup_layout.add_widget(content)
        content.bind(on_press=popup.dismiss)
    return popup


class AimaUI(App):

    """Class to manage aima agents and environments."""

    def __init__(self):
        """Initialize the user interface."""
        App.__init__(self)
        self.scoreA = 0
        self.scoreB = 0
        self.agentA = "Agent A"
        self.agentAImgDef = "img/agentA_v0.png"
        self.agentAImg = None
        self.agentB = "Agent B"
        self.agentBImgDef = "img/agentB_v0.png"
        self.agentBImg = None
        self.wall_img = Image(source="img/wall.png")
        self.trash_img = Image(source="img/trash.png")
        self.map = None
        self.running = False
        self.env = None
        self.counter_steps = 0
        self.initialized = False

    def __initialize_env(self):
        """Initialize aima environment."""
        if self.env is not None:
            del self.env
            self.env = None
        if self.map is not None:
            self.env = ALL_MAPS[self.map]()
        if self.agentA in ALL_AGENTS:
            agent_A = TraceAgent(ALL_AGENTS[self.agentA]())
            if agent_A.img is not None and check_img(agent_A.img):
                self.agentAImg = Image(
                    source=path.join("agents_dir", path.join("img", agent_A.img)))
            else:
                self.agentAImg = Image(source=self.agentAImgDef)
            self.env.add_thing(agent_A, location=self.env.start_from)
        if self.agentB in ALL_AGENTS:
            agent_B = TraceAgent(ALL_AGENTS[self.agentB]())
            if agent_B.img is not None and check_img(agent_B.img):
                self.agentBImg = Image(
                    source=path.join("agents_dir", path.join("img", agent_B.img)))
            else:
                self.agentBImg = Image(source=self.agentBImgDef)
            self.env.add_thing(agent_B, location=self.env.start_from)

    def get_scores(self):
        """Get agents' scores."""
        return ("ScoreA = {0:d}".format(self.scoreA),
                "ScoreB = {0:d}".format(self.scoreB))

    def update_canvas(self, labels, wid, *largs):
        """Update the canvas to respect the environment."""
        wid.canvas.clear()
        self.counter.text = str(self.counter_steps)
        n_x, n_y = max([thing.location for thing in self.env.things])
        tile_x = wid.width / (n_x + 1)
        tile_y = wid.height / (n_y + 1)
        labelA, labelB = labels
        with wid.canvas:
            for thing in [thing for thing in self.env.things
                          if isinstance(thing, Dirt) or
                          isinstance(thing, Clean)]:
                pos_y, pos_x = thing.location
                if isinstance(thing, Dirt):
                    Color(0.5, 0, 0)
                    Rectangle(
                        pos=(
                            pos_x * tile_x + wid.x,
                            n_y * tile_y - pos_y * tile_y + wid.y),
                        size=(tile_x, tile_y))
                    Color(1, 1, 1, 1)
                    Rectangle(texture=self.trash_img.texture,
                              pos=(
                                  pos_x * tile_x + wid.x + (tile_x / 4),
                                  n_y * tile_y - pos_y *
                                  tile_y + wid.y + (tile_y / 4)
                              ),
                              size=(tile_x / 2, tile_y / 2))
                elif isinstance(thing, Clean):
                    Color(0.1, 0.5, 0.1)
                    Rectangle(
                        pos=(
                            pos_x * tile_x + wid.x,
                            n_y * tile_y - pos_y * tile_y + wid.y),
                        size=(tile_x, tile_y))
            for thing in [thing for thing in self.env.things
                          if isinstance(thing, Wall)]:
                pos_y, pos_x = thing.location
                Color(1, 1, 1, 1)
                Rectangle(texture=self.wall_img.texture,
                          pos=(pos_x * tile_x + wid.x,
                               n_y * tile_y - pos_y * tile_y + wid.y),
                          size=(tile_x, tile_y))
            for thing in [thing for thing in self.env.things
                          if isinstance(thing, ALL_AGENTS.get(self.agentA, Agent)) or
                          isinstance(thing, ALL_AGENTS.get(self.agentB, Agent))]:
                pos_y, pos_x = thing.location
                if self.agentA in ALL_AGENTS and\
                   isinstance(thing, ALL_AGENTS[self.agentA]):
                    self.scoreA = thing.performance
                    labelA.text = self.get_scores()[0]
                    Color(1, 1, 1, 1)
                    Rectangle(texture=self.agentAImg.texture,
                              pos=(pos_x * tile_x + wid.x,
                                   n_y * tile_y - pos_y * tile_y + wid.y),
                              size=(tile_x, tile_y))
                if self.agentB in ALL_AGENTS and\
                   isinstance(thing, ALL_AGENTS[self.agentB]):
                    self.scoreB = thing.performance
                    labelB.text = self.get_scores()[1]
                    Color(1, 1, 1, 1)
                    Rectangle(texture=self.agentBImg.texture,
                              pos=(pos_x * tile_x + wid.x,
                                   n_y * tile_y - pos_y * tile_y + wid.y),
                              size=(tile_x, tile_y))

    def load_env(self, labels, wid, *largs):
        """Load and prepare the environment."""
        self.running = False
        self.counter_steps = 0
        if self.map is None or self.map == "Maps":
            gen_popup("Error!", "No map selected...").open()
            return
        elif self.agentA not in ALL_AGENTS and\
                self.agentB not in ALL_AGENTS:
            gen_popup("Error!", "You must choose at least one agent...").open()
            return
        self.__initialize_env()
        self.initialized = True
        self.update_canvas(labels, wid)

    def running_step(self, labels, wid, n_step=None, *largs):
        """Run the program of the environment, called from run."""
        if self.env is not None:
            if n_step is not None:
                if self.counter_steps == n_step:
                    self.running = False
                    self.btn_100step.state = "normal"
                    self.counter_steps = 0
                    return False
                else:
                    self.counter_steps += 1
            if not self.running:
                return False
            self.env.step()
            self.update_canvas(labels, wid)

    def btn_step(self, labels, wid, *largs):
        """Update the environment one step."""
        if not self.initialized:
            gen_popup("Error!", "You must load a map...").open()
            return
        elif self.agentA == "Agent A" and self.agentB == "Agent B":
            popup = gen_popup(
                "Error!", "Agent not selected, reset required...", False).open()
            Clock.schedule_once(popup.dismiss, timeout=2)
            Clock.schedule_once(self.partial_reset, timeout=2)
            return
        if self.env is not None:
            self.env.step()
            self.update_canvas(labels, wid)

    def btn_100step(self, function, labels, wid, *largs):
        """Update the environment one step."""
        if not self.initialized:
            gen_popup("Error!", "You must load a map...").open()
            self.btn_100step.state = "normal"
            return
        elif self.agentA == "Agent A" and self.agentB == "Agent B":
            popup = gen_popup(
                "Error!", "Agent not selected, reset required...", False).open()
            Clock.schedule_once(popup.dismiss, timeout=2)
            Clock.schedule_once(self.partial_reset, timeout=2)
        self.btn_100step.state = "down"
        self.running = True
        Clock.schedule_interval(partial(function, labels, wid, 100), 1 / 30.)

    def btn_run(self, function, labels, wid, *largs):
        """Run a function for the update."""
        if not self.initialized:
            gen_popup("Error!", "You must load a map...").open()
            self.btn_run.state = "normal"
            return
        elif self.agentA == "Agent A" and self.agentB == "Agent B":
            popup = gen_popup(
                "Error!", "Agent not selected, reset required...", False).open()
            Clock.schedule_once(popup.dismiss, timeout=2)
            Clock.schedule_once(self.partial_reset, timeout=2)
        self.btn_run.state = "down"
        self.running = True
        Clock.schedule_interval(partial(function, labels, wid), 1 / 30.)

    def btn_stop(self, function, *largs):
        """Stop a specific fuction."""
        if not self.initialized:
            gen_popup("Error!", "You must load a map...").open()
            return
        elif self.agentA == "Agent A" and self.agentB == "Agent B":
            popup = gen_popup(
                "Error!", "Agent not selected, reset required...", False).open()
            Clock.schedule_once(popup.dismiss, timeout=2)
            Clock.schedule_once(self.partial_reset, timeout=2)
        self.running = False
        self.counter_steps = 0
        self.btn_run.state = "normal"
        self.btn_100step.state = "normal"
        Clock.unschedule(function)

    @staticmethod
    def reset_popup(popup, *largs):
        popup.dismiss()
        gen_popup("INFO", "Reset done!!!").open()

    def reset_all(self, labels, spinners, wid, *largs):
        """Clear the entire environment."""
        popup = gen_popup("WARNING!", "I'm deleting everything!!!", False)
        popup.open()
        self.initialized = False
        self.agentA = "Agent A"
        self.agentB = "Agent B"
        self.map = None
        self.running = False
        self.counter_steps = 0
        self.scoreA = 0
        self.scoreB = 0
        self.__initialize_env()
        wid.canvas.clear()
        labelA, labelB = labels
        labelA.text = self.get_scores()[0]
        labelB.text = self.get_scores()[1]
        reload(envs_list)
        reload(agents_list)
        global ALL_AGENTS
        global ALL_MAPS
        ALL_AGENTS = agents_list.load_agents()
        ALL_MAPS = envs_list.ALL_MAPS
        spinnerA, spinnerB, spinnerMap = spinners
        spinnerA.values = sorted(
            [agent for agent in list(ALL_AGENTS.keys())]) + ["Agent A"]
        spinnerB.values = sorted(
            [agent for agent in list(ALL_AGENTS.keys())]) + ["Agent B"]
        spinnerMap.values = sorted(
            [map for map in list(ALL_MAPS.keys())]) + ["Maps"]
        spinnerA.text = "Agent A"
        spinnerB.text = "Agent B"
        spinnerMap.text = "Maps"
        self.counter.text = str(self.counter_steps)
        Clock.schedule_once(partial(self.reset_popup, popup), timeout=1)

    def on_resize(self, width, eight):
        self.update_canvas()

    def select_agent_A(self, spinner, text):
        self.agentA = text

    def select_agent_B(self, spinner, text):
        self.agentB = text

    def select_map(self, spinner, text):
        self.map = text

    def on_resize(self, width, eight, test):
        if self.initialized:
            Clock.schedule_once(
                partial(self.update_canvas, self.labels, self.wid))

    def build(self):
        """Build the user interface."""

        wid = Widget()

        self.counter = Label(text="0")
        labelA = Label(text=self.get_scores()[0])
        labelB = Label(text=self.get_scores()[1])
        labels = (labelA, labelB)
        self.labels = labels
        self.wid = wid

        agentA_spinner = Spinner(
            text='Agent A',
            text_size=(95, None),
            haligh="center",
            shorten=True,
            values=sorted([agent for agent in list(ALL_AGENTS.keys())]) +
            ["Agent A"],
            size=(100, 44)
        )

        agentB_spinner = Spinner(
            text='Agent B',
            text_size=(95, None),
            shorten=True,
            values=sorted([agent for agent in list(ALL_AGENTS.keys())]) +
            ["Agent B"],
            size=(100, 44)
        )

        maps_spinner = Spinner(
            text='Maps',
            text_size=(95, None),
            shorten=True,
            values=sorted([map for map in list(ALL_MAPS.keys())]) + ["Maps"],
            size=(100, 44)
        )

        agentA_spinner.bind(text=self.select_agent_A)
        agentB_spinner.bind(text=self.select_agent_B)
        maps_spinner.bind(text=self.select_map)

        btn_load = Button(text='Load',
                          on_press=partial(self.load_env, labels, wid))

        btn_step = Button(text='Step >',
                          on_press=partial(self.btn_step, labels, wid))

        self.btn_100step = ToggleButton(text='100 Step >',
                                        on_press=partial(self.btn_100step,
                                                         self.running_step,
                                                         labels,
                                                         wid))

        self.btn_run = ToggleButton(
            text='Run >>', on_press=partial(self.btn_run,
                                            self.running_step,
                                            labels,
                                            wid))

        btn_stop = Button(text='Stop [ ]',
                          on_press=partial(self.btn_stop,
                                           self.running_step))

        self.partial_reset = partial(self.reset_all,
                                     labels,
                                     (agentA_spinner,
                                      agentB_spinner, maps_spinner),
                                     wid)

        btn_reset = Button(text='Reset',
                           on_press=self.partial_reset)

        Window.bind(on_resize=self.on_resize)

        action_layout = BoxLayout(size_hint=(1, None), height=50)
        action_layout.add_widget(btn_load)
        action_layout.add_widget(btn_step)
        action_layout.add_widget(self.btn_100step)
        action_layout.add_widget(self.counter)
        action_layout.add_widget(self.btn_run)
        action_layout.add_widget(btn_stop)
        action_layout.add_widget(btn_reset)

        agents_layout = BoxLayout(size_hint=(1, None), height=50)
        agents_layout.add_widget(agentA_spinner)
        agents_layout.add_widget(labelA)
        agents_layout.add_widget(agentB_spinner)
        agents_layout.add_widget(labelB)
        agents_layout.add_widget(maps_spinner)

        root = BoxLayout(orientation='vertical')
        root.add_widget(wid)
        root.add_widget(action_layout)
        root.add_widget(agents_layout)

        return root

if __name__ == '__main__':
    AimaUI().run()
