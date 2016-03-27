# -*- coding:utf-8 -*-

import sys
import inspect
import pkgutil

__all__ = ["load_agents"]

#
# All Agents TABLE
ALL_AGENTS = {}

import agents_dir

def load_agents():
    reload(agents_dir)
    for importer, modname, ispkg in pkgutil.iter_modules(agents_dir.__path__):
        for name, obj in inspect.getmembers(
                sys.modules['agents_dir.{0}'.format(modname)],
                inspect.isclass):
            if 'agents_dir.{0}'.format(modname) == obj.__module__ and\
                    '{0}Class'.format(modname) == name and \
                    issubclass(obj, agents_dir.Agent):
                ALL_AGENTS[modname] = obj

    return ALL_AGENTS
