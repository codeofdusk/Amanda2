"An internal module for managing config files."

import os
import configobj
from validate import Validator

conf = None


def load(path="amanda2.conf", specpath="config.spec", validate=True):
    "Loads and validates user configuration. Populates the module-level conf variable for use in other parts of the program and does not return. If validate is True, call validate_config() when the config is loaded."
    global conf
    new = not os.path.exists(path)
    conf = configobj.ConfigObj(path, configspec=specpath)
    if validate:
        validate_config()
    if new:
        print(
            "This appears to be the first time you have run Amanda on this system. A default configuration file has been written to "
            + path +
            ". Please edit it for your use case and re-run Amanda when finished."
        )


def validate_config():
    "Validates and writes back user configuration if available."
    global conf
    if conf is None:
        print("Warning: config validation attempted before load")
        return
    val = Validator()
    v = conf.validate(val, copy=True)
    if not v:
        raise ValueError("Invalid user configuration.")
    else:
        conf.write()
