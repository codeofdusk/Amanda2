"An internal module for managing config files."

import os
import configobj
from validate import Validator

conf = None
configured = None
val = Validator()


def load(path="amanda2.conf", specpath="config.spec"):
    "Loads and validates user configuration. Populates the module-level conf variable for use in other parts of the program and does not return."
    global conf, new
    new = not os.path.exists(path)
    conf = configobj.ConfigObj(path, configspec=specpath)
    v = conf.validate(val, copy=new)
    if not v:
        raise ValueError("Invalid user configuration.")
    elif new:
        conf.write()
        print(
            "This appears to be the first time you have run Amanda on this system. A default configuration file has been written to " +
            path +
            ". Please edit it for your use case and re-run Amanda when finished.")
