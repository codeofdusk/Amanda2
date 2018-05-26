"Manages Amanda components (plugins and drivers)."

import config
import os
import importlib

plugins = []
drivers = []


def _discover(type, basepath=None):
    "An internal use function to discover Amanda components and add config sections where required. If basepath is specified, that path is searched for source files, otherwise the default path is used. Returns True if new components are discovered, False otherwise."
    path = os.path.join(basepath, type + "s")
    t = []
    for i in os.listdir(path):
        p = os.path.splitext(i)
        if p[1] == '.py' and p[0] != '__init__' and p[0] != 'Base' + \
                type.capitalize():
            t.append(p[0])
    if type + "s" not in config.conf:
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


def _import(path):
    "Imports and returns the module from the given path."
    p = os.path.split(path)
    packagename = os.path.basename(p[0])
    modname = os.path.splitext(p[1])[0]
    spec = importlib.util.spec_from_file_location(
        packagename + "." + modname, path)
    res = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(res)
    return res


def _loadtype(type, basepath):
    "An internal-use function to instantiate components of a given type."
    # Get the list of discovered components.
    c = config.conf[type + 's']
    disc = c.sections
    # Get the list of enabled components.
    enabled = [i for i in disc if c[i].as_bool(
        'enabled') and c[i] != 'Base' + type.capitalize()]
    # Get a list of paths
    paths = [os.path.join(basepath, type + "s", i + ".py") for i in enabled]
    # Import and instantiate
    mods = map(_import, paths)
    res = []
    for mod in mods:
        b = None
        for name, obj in mod.__dict__.items():
            if name == "Base" + type.capitalize():
                b = obj
            if hasattr(obj, "__bases__") and b in obj.__bases__:
                # Instantiate the component, passing all config options (except
                # enabled) as kwargs.
                kwargs = dict(
                    config.conf[type + 's'][os.path.splitext(os.path.basename(mod.__file__))[0]])
                del kwargs['enabled']
                inst = obj(**kwargs)
                res.append(inst)
    return res


def load(basepath=None):
    "Instantiates plugins and drivers based on user configuration. If basepath is specified, that directory will be searched for components, otherwise the current directory will be searched. Returns the result of _discover for (True if new plugins, drivers, or both have been discovered)."
    global plugins, drivers
    if basepath is None:
        basepath = ''
    newd = _discover('driver', basepath=basepath)
    drivers = _loadtype('driver', basepath)
    newp = _discover('plugin', basepath=basepath)
    plugins = _loadtype('plugin', basepath)
    return newd or newp
