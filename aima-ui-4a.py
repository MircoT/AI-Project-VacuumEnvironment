'''
Canvas stress
=============

This example tests the performance of our Graphics engine by drawing large
numbers of small sqaures. You should see a black canvas with buttons and a
label at the bottom. Pressing the buttons adds small colored squares to the
canvas.

'''
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.splitter import Splitter
from kivy.uix.image import Image
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.popup import Popup

from random import random as r
from functools import partial
from os import path, walk
from agent_dir import *

import agent_list
import env_list


def gen_popup(title, text, dismiss=True):
    """Generate a popup."""
    popup_layout = BoxLayout(orientation='vertical')
    content = Button(text='Close', size_hint=(1, .3))
    popup_layout.add_widget(Label(text=text))
    popup = Popup(title=title,
                  content=popup_layout)
    if dismiss:
        popup_layout.add_widget(content)
        content.bind(on_press=popup.dismiss)
    return popup


class Renderer(Widget):

    def __init__(self):
        super(Renderer, self).__init__()
        self._imgs = {}
        self._tile_size = (0, 0)

        self.add_images_from_folder(self._imgs, './img')
        self.add_images_from_folder(self._imgs, './agent_dir/img')

    def add_images_from_folder(self, container, folder):
        images = {}

        for root, dirs, files in walk(path.abspath(folder)):
            for file_ in files:
                name, ext = path.splitext(path.basename(file_))
                if ext == '.png':
                    images[name] = Image(source=path.join(root, file_))

        container.update(images)

    def real_pos(self, x, y):
        return (self.x + x * self._tile_size[0],
                self.y + y * self._tile_size[1])

    def set_tile_size(self, env):
        if env is not None:
            n_x, n_y = max([thing.location for thing in env.things])
            tile_x = self.width / float(n_x + 1)
            tile_y = self.height / float(n_y + 1)
            self._tile_size = (tile_x, tile_y)

    def clear(self):
        self.canvas.clear()

    def draw(self, env):
        self.clear()

        if env is not None:
            walls = []
            dirts = []
            cleans = []
            agents = []

            for thing in env.things:
                if isinstance(thing, Wall):
                    walls.append(thing)
                elif isinstance(thing, Dirt):
                    dirts.append(thing)
                elif isinstance(thing, Clean):
                    cleans.append(thing)
                elif isinstance(thing, Agent):
                    agents.append(thing)

            with self.canvas:
                for wall in walls:
                    Rectangle(texture=self._imgs.get('wall').texture,
                              pos=self.real_pos(*wall.location),
                              size=self._tile_size)
                for dirt in dirts:
                    Color(0.9, 0, 0, 0.6)
                    Rectangle(
                        pos=self.real_pos(*dirt.location),
                        size=self._tile_size)
                    Color(1, 1, 1, 1)
                    Rectangle(texture=self._imgs.get('trash').texture,
                              pos=self.real_pos(*dirt.location),
                              size=self._tile_size)
                for clean in cleans:
                    Color(0, 0.9, 0, 0.6)
                    Rectangle(
                        pos=self.real_pos(*clean.location),
                        size=self._tile_size)
                for agent in agents:
                    Color(1, 1, 1, 1)
                    Rectangle(
                        texture=self._imgs.get(agent.img if agent.img is not None else agent.id.lower()).texture,
                        pos=self.real_pos(*agent.location),
                        size=self._tile_size)



class ToggleButton(ToggleButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ToggleButton, self).__init__(**kwargs)
        self.source = 'atlas://data/images/defaulttheme/checkbox_off'

    def on_state(self, widget, value):
        if value == 'down':
            self.source = 'atlas://data/images/defaulttheme/checkbox_on'
        else:
            self.source = 'atlas://data/images/defaulttheme/checkbox_off'



class VacuumEnv(App):

    def __init__(self, **kwargs):
        super(VacuumEnv, self).__init__(**kwargs)
        self._agents = {}
        self._maps = {}
        self._wid = None
        self._env = None
        self._step = 0
        self._100_steps_pressed = False
        self._agent_objs = {
            'agent_1': None,
            'agent_2': None,
            'agent_3': None,
            'agent_4': None
        }

        self._loading = gen_popup("WARNING", "Loading...", dismiss=False)
        self._load_done = gen_popup("INFO", "All resources loaded", dismiss=True)

    def _resize_env(self, *largs):
        self._wid.set_tile_size(self._env)
        self._wid.draw(self._env)

    def on_resize(self, window, width, height, *largs):
        Clock.schedule_once(self._resize_env)

    def splitter_on_release(self):
        self._wid.set_tile_size(self._env)
        self._wid.draw(self._env)

    def splitter_on_press(self):
        self._wid.set_tile_size(self._env)
        self._wid.draw(self._env)

    def load_agents_and_maps(self, spinner_list, spinner_map):
        self._loading.open()
        self._agents = agent_list.load_agents()
        self._maps = env_list.get_maps()

        for num, spinner in enumerate(spinner_list, 1):
            spinner.values =["agent_{0}".format(num)] + [elm for elm in sorted(self._agents.keys())]

        spinner_map.values = [elm for elm in sorted(self._maps.keys())] + ['Maps']
        self._loading.dismiss()
        self._load_done.open()

    def select_map(self, t_btn_random, label_steps, instance, data, *largs):
        self._wid.clear()
        self._env = self._maps.get(data, None)
        if self._env is not None:
            self._env = self._env()
            self._step = 0
            label_steps.text = '{0}'.format(self._step)
            for name, agent in self._agent_objs.items():
                agent.__init__()
                if agent is not None:
                    if t_btn_random.state == 'down':
                        self._env.add_thing(agent,
                                            location=self._env.random_location())
                    else:
                        self._env.add_thing(agent,
                                            location=self._env.start_from)
        self._wid.set_tile_size(self._env)
        self._wid.draw(self._env)

    def select_agent(self, agent_id, t_btn_random, spinner, text, *largs):
        if text in ['agent_1', 'agent_2', 'agent_3', 'agent_4']:
            spinner.text = agent_id
            if self._env is not None and self._agent_objs[agent_id] is not None:
                self._env.delete_thing(self._agent_objs[agent_id])
            self._agent_objs[agent_id] = None
        else:
            if self._agent_objs[agent_id] is not None:
                self._env.delete_thing(self._agent_objs[agent_id])
            self._agent_objs[agent_id] = self._agents[text]()
            self._agent_objs[agent_id].id = agent_id
            if self._env is not None:
                if t_btn_random.state == 'down':
                    self._env.add_thing(self._agent_objs[agent_id],
                                        location=self._env.random_location())
                else:
                    self._env.add_thing(self._agent_objs[agent_id],
                                        location=self._env.start_from)
        self._wid.draw(self._env)

    def step(self, *largs, **kwargs):
        if self._env is not None:
            self._env.step()
            self._wid.draw(self._env)
            self._step += 1
            kwargs['label_steps'].text = '{0}'.format(self._step)
            for id_, label in kwargs['label_agents'].items():
                if self._agent_objs[id_] is not None:
                    label.text = "{0}".format(self._agent_objs[id_].performance)

    def evt_100_steps(self, steps, *largs, **kwargs):
        if self._env is not None:
            if not self._100_steps_pressed and steps == 100:
                self._100_steps_pressed = True
                kwargs['btn_100step'].state = 'down'
                self.step(*largs, **kwargs)
                Clock.schedule_once(partial(self.evt_100_steps, steps-1, *largs, **kwargs), 1. / 30.)
            elif steps < 100:
                if steps == 0:
                    kwargs['btn_100step'].state = 'normal'
                    self._100_steps_pressed = False
                else:
                    kwargs['btn_100step'].state = 'down'
                    self.step(*largs, **kwargs)
                    Clock.schedule_once(partial(self.evt_100_steps, steps-1, *largs, **kwargs), 1. / 30.)

    def evt_step(self, *largs, **kwargs):
        Clock.schedule_once(partial(self.step, *largs, **kwargs))

    def reset(self, spinn_map, t_btn_random, label_steps, spinn_agents, label_agents, *largs, **kwargs):
        self._wid.clear()
        self._step = 0
        label_steps.text = '{0}'.format(self._step)
        for label in label_agents:
            label.text = '{0}'.format(self._step)
        self._env = self._maps.get(spinn_map.text, None)
        if self._env is not None:
            self._env = self._env()
            for spinner in spinn_agents:
                if spinner.text not in ['agent_1', 'agent_2', 'agent_3', 'agent_4']:
                    self._agent_objs[spinner.id] = self._agents[spinner.text]()
                    self._agent_objs[spinner.id].id = spinner.id
                    if t_btn_random.state == 'down':
                        self._env.add_thing(self._agent_objs[spinner.id],
                                            location=self._env.random_location())
                    else:
                        self._env.add_thing(self._agent_objs[spinner.id],
                                                location=self._env.start_from)
            self._wid.set_tile_size(self._env)
            self._wid.draw(self._env)

    def build(self):
        self._wid = Renderer()

        ##
        # First row
        label_steps = Label(text='{0}'.format(self._step), color=(0.1, 1, 0.1, 1))

        btn_load = Button(text='Load')

        btn_step = Button(text='Step >')

        btn_100step = Button(text='100 Step >')

        spinn_map = Spinner(
            text='Maps',
            shorten=True,
            shorten_from='right',
            halign='left',
            text_size=(64, None),
            values=["Maps"]
        )

        label_random_pos = Label(text='rand p', size=(100, 42), size_hint=(None, 1))
        t_btn_random = ToggleButton(size=(64, 42), size_hint=(None, 1))

        btn_reset = Button(text='Reset')

        lay_splitter = BoxLayout(orientation='vertical')

        ##
        # Second row
        spinn_agent_01 = Spinner(
            id='agent_1',
            text='agent_1',
            shorten=True,
            shorten_from='right',
            text_size=(200, None),
            values=["agent_1"]
        )

        label_agent_01 = Label(text='0')

        spinn_agent_02 = Spinner(
            id='agent_2',
            text='agent_2',
            shorten=True,
            shorten_from='right',
            text_size=(200, None),
            values=["agent_1"]
        )

        label_agent_02 = Label(text='0')

        ##
        # Third row
        spinn_agent_03 = Spinner(
            id='agent_3',
            text='agent_3',
            shorten=True,
            shorten_from='right',
            text_size=(200, None),
            values=["agent_1"]
        )

        label_agent_03 = Label(text='0')

        spinn_agent_04 = Spinner(
            id='agent_4',
            text='agent_4',
            shorten=True,
            shorten_from='right',
            text_size=(200, None),
            values=["agent_1"]
        )

        label_agent_04 = Label(text='0')

        ##
        # Layout
        lay_actions = BoxLayout()
        lay_actions.add_widget(btn_load)
        lay_actions.add_widget(btn_step)
        lay_actions.add_widget(btn_100step)
        lay_actions.add_widget(label_steps)
        lay_actions.add_widget(spinn_map)
        lay_actions.add_widget(label_random_pos)
        lay_actions.add_widget(t_btn_random)
        lay_actions.add_widget(btn_reset)

        lay_splitter.add_widget(lay_actions)

        lay_agent_row_0 = BoxLayout()
        lay_agent_row_0.add_widget(spinn_agent_01)
        lay_agent_row_0.add_widget(label_agent_01)
        lay_agent_row_0.add_widget(label_agent_02)
        lay_agent_row_0.add_widget(spinn_agent_02)

        lay_agent_row_1 = BoxLayout()
        lay_agent_row_1.add_widget(spinn_agent_03)
        lay_agent_row_1.add_widget(label_agent_03)
        lay_agent_row_1.add_widget(label_agent_04)
        lay_agent_row_1.add_widget(spinn_agent_04)

        lay_splitter.add_widget(lay_agent_row_0)
        lay_splitter.add_widget(lay_agent_row_1)

        splitter = Splitter(sizable_from='top')
        splitter.add_widget(lay_splitter)
        splitter.min_size = 128
        splitter.size_hint_y = 0.16

        root = BoxLayout(orientation='vertical')
        root.add_widget(self._wid)
        root.add_widget(splitter)

        Window.minimum_width = 640
        Window.minimum_height = 480

        ##
        # Events
        Window.bind(on_resize=self.on_resize)

        btn_load.on_press = partial(self.load_agents_and_maps,
                                    [spinn_agent_01,
                                     spinn_agent_02,
                                     spinn_agent_03,
                                     spinn_agent_04],
                                    spinn_map)

        btn_step.on_press = partial(self.evt_step,
                                    label_steps=label_steps,
                                    label_agents={
                                        'agent_1': label_agent_01,
                                        'agent_2': label_agent_02,
                                        'agent_3': label_agent_03,
                                        'agent_4': label_agent_04,
                                    })

        btn_100step.on_press = partial(self.evt_100_steps, 100,
                                       label_steps=label_steps,
                                       btn_100step=btn_100step,
                                       label_agents={
                                           'agent_1': label_agent_01,
                                           'agent_2': label_agent_02,
                                           'agent_3': label_agent_03,
                                           'agent_4': label_agent_04,
                                       })

        btn_reset.on_press = partial(self.reset,
                                     spinn_map,
                                     t_btn_random,
                                     label_steps,
                                     [
                                        spinn_agent_01,
                                        spinn_agent_02,
                                        spinn_agent_03,
                                        spinn_agent_04
                                     ],
                                     [
                                         label_agent_01,
                                         label_agent_02,
                                         label_agent_03,
                                         label_agent_04,
                                     ])

        spinn_map.bind(text=partial(self.select_map, t_btn_random, label_steps))
        spinn_agent_01.bind(text = partial(self.select_agent, spinn_agent_01.id, t_btn_random,))
        spinn_agent_02.bind(text = partial(self.select_agent, spinn_agent_02.id, t_btn_random,))
        spinn_agent_03.bind(text = partial(self.select_agent, spinn_agent_03.id, t_btn_random,))
        spinn_agent_04.bind(text = partial(self.select_agent, spinn_agent_04.id, t_btn_random,))

        splitter.on_press = partial(self.splitter_on_press)
        splitter.on_release = partial(self.splitter_on_release)

        return root

if __name__ == '__main__':
    VacuumEnv().run()
