"Manages Amanda components (plugins and drivers)."
import config
import os

plugins = []
drivers = []


def discover(type, basepath=None):
    "Discover Amanda components and add config sections where required. If basepath is specified, that path is searched for source files, otherwise the default path is used. Returns True if new components are discovered, False otherwise."
    if basepath is None:
        basepath = ''
    path = os.path.join(basepath, type + "s")
    t = []
    for i in os.listdir(path):
        p = os.path.splitext(i)
        if p[1] == '.py' and p[0] != '__init__' and p[0] != 'Base' + \
                type.capitalize():
            t.append(p[0])
    if type + "s" not in conf:
        config.conf[type + "s"] = {}
    s = config.conf[type + "s"]
    # Get the return value
    new = s.sections != t
    # Add new sections if needed
    if new:
        for i in t:
            if i not in s:
                s[i] = {'enabled': False}
        # Write new config to disk
        config.conf.write()
    return new
