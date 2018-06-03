"Manages Amanda components (plugins and drivers)."

import os
import importlib
import configobj
import config
import collections

plugins = []
drivers = []


def _import(path):
    "Imports and returns the module from the given path."
    p = os.path.split(path)
    packagename = os.path.basename(p[0])
    modname = os.path.splitext(p[1])[0]
    spec = importlib.util.spec_from_file_location(packagename + "." + modname,
                                                  path)
    res = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(res)
    return res


def _discover(type, basepath):
    "An internal use function to discover Amanda components and import the modules that contain them. If basepath is specified, that path is searched for source files, otherwise the default path is used. Returns a list of modules containing components of the given type."
    path = os.path.join(basepath, type + "s")
    t = []
    for i in os.listdir(path):
        p = os.path.splitext(i)
        if p[1] == '.py' and p[0] != '__init__' and p[0] != \
                'Base' + type.capitalize():
            t.append(os.path.join(path, i))
    return [_import(i) for i in t]


def _get_short_name(m):
    "Returns the short name (filename without path, package, or extension) of an imported module. This name is used in the config and discovery systems to identify components."
    return m.__name__.split(".")[-1]


def _merge(base, indict, decoupled=False):
    "A patched version of configobj.section.merge which also copies comments. Waiting for this to be merged upstream."
    for key, val in list(indict.items()):
        if decoupled:
            val = copy.deepcopy(val)
        if (key in base and isinstance(base[key], collections.Mapping)
                and isinstance(val, collections.Mapping)):
            _merge(base[key], val, decoupled=decoupled)
            if hasattr(val, 'comments') and isinstance(val.comments,
                                                       collections.Mapping):
                base[key].comments.update(val.comments)
            if hasattr(val, 'inline_comments') and isinstance(
                    val.inline_comments, collections.Mapping):
                base[key].inline_comments.update(val.inline_comments)
        else:
            base[key] = val
        if hasattr(indict, 'comments') and isinstance(
                indict.comments, collections.Mapping
        ) and key in indict.comments and key not in base.comments:
            base.comments[key] = indict.comments[key]
        if hasattr(indict, 'inline_comments') and isinstance(
                indict.inline_comments, collections.Mapping
        ) and key in indict.inline_comments and key not in base.inline_comments:
            base.inline_comments[key] = indict.inline_comments[key]


def _configure(type, discovered):
    "Updates user configuration based on discovered components."
    if type + "s" not in config.conf:
        config.conf[type + "s"] = {}
    for m in discovered:
        head = '[' + type + 's]'
        sectionname = '[[' + _get_short_name(m) + ']]'
        if hasattr(m, 'configspec'):
            cs = m.configspec
        else:
            # No config spec provided by the plugin maintainer, so use this default.
            cs = (head, sectionname, 'enabled=boolean(default=False)')
        if head not in cs:
            cs = (head, *cs)
        if sectionname not in cs:
            cs = (sectionname, *cs)
        spec = configobj.ConfigObj(cs, _inspec=True)
        # Clean the config spec
        typesec = spec[spec.sections[0]]
        compsec = typesec[typesec.sections[0]]
        if len(spec.sections) != 1 or len(typesec) != 1:
            raise ValueError(
                "Config spec for " + m.__name__ +
                " has wrong number of config sections. This may be a security concern!"
            )
        # Always supply enabled and set to False to prevent components from overriding.
        compsec['enabled'] = 'boolean(default=False)'
        # All checks passed, so merge the component spec and user config spec.
        _merge(config.conf.configspec, spec)


def _loadtype(type, basepath, discovered=None):
    "An internal-use function to instantiate components of a given type."
    # Get the list of configured components.
    c = config.conf[type + 's']
    disc = c.sections
    # Get the list of enabled components.
    enabled = [
        i for i in disc
        if c[i].as_bool('enabled') and c[i] != 'Base' + type.capitalize()
    ]
    # Filter imported modules to only those containing enabled components.
    if not discovered:
        discovered = _discover(type, basepath)
    mods = [m for m in discovered if _get_short_name(m) in enabled]
    res = []
    for mod in mods:
        b = None
        for name, obj in mod.__dict__.items():
            if name == "Base" + type.capitalize():
                b = obj
                break
        for name, obj in mod.__dict__.items():
            if hasattr(obj, "__bases__") and b in obj.__bases__:
                # Instantiate the component, passing config parameters (except enabled) as kwargs
                kwargs = dict(config.conf[type + 's'][_get_short_name(mod)])
                del kwargs['enabled']
                inst = obj(**kwargs)
                res.append(inst)
    return res


def load(basepath=None):
    "Instantiates plugins and drivers based on user configuration. If basepath is specified, that directory will be searched for components, otherwise the current directory will be searched. Returns the result of _configure for (True if new plugins, drivers, or both have been discovered)."
    global plugins, drivers
    if basepath is None:
        basepath = ''
    # Store the length of the root type sections to allow for auto-detection.
    driverconf = config.conf["drivers"]
    beforedrivers = len(driverconf)
    pluginconf = config.conf["plugins"]
    beforeplugins = len(pluginconf)
    _configure('driver', _discover('driver', basepath=basepath))
    _configure('plugin', _discover('plugin', basepath=basepath))
    config.validate_config()
    drivers = _loadtype('driver', basepath)
    plugins = _loadtype('plugin', basepath)
    return len(driverconf) != beforedrivers or len(pluginconf) != beforeplugins
