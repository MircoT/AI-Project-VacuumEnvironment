# -*- coding:utf-8 -*-

import sys
import inspect
import pkgutil
if sys.version_info.major > 2:
    from importlib import reload

import agents_dir

__all__ = ["load_agents"]



def load_agents():

    for importer, modname, ispkg in pkgutil.iter_modules(agents_dir.__path__):
        if modname != 'agents':
            reload(sys.modules['{0}.AvalonVacuumAgent'.format('agents_dir')])

    all_agents = {}

    for importer, modname, ispkg in pkgutil.iter_modules(agents_dir.__path__):
        for name, obj in inspect.getmembers(
                sys.modules['agents_dir.{0}'.format(modname)],
                inspect.isclass):
            if 'agents_dir.{0}'.format(modname) == obj.__module__ and\
                    '{0}Class'.format(modname) == name and\
                    issubclass(obj, agents_dir.Agent):
                all_agents[modname] = obj

    return all_agents
