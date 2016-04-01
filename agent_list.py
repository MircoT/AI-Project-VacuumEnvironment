# -*- coding:utf-8 -*-

import sys
import inspect
import pkgutil
if sys.version_info.major > 2:
    from importlib import reload

import agent_dir

__all__ = ["load_agents"]



def load_agents():

    for importer, modname, ispkg in pkgutil.iter_modules(agent_dir.__path__):
        if modname != 'agents':
            reload(sys.modules['{0}.{1}'.format('agent_dir', modname)])

    all_agents = {}

    for importer, modname, ispkg in pkgutil.iter_modules(agent_dir.__path__):
        for name, obj in inspect.getmembers(
                sys.modules['agent_dir.{0}'.format(modname)],
                inspect.isclass):
            if 'agent_dir.{0}'.format(modname) == obj.__module__ and\
                    '{0}Class'.format(modname) == name and\
                    issubclass(obj, agent_dir.Agent):
                all_agents[modname] = obj

    return all_agents
