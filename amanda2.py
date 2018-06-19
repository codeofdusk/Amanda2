"Amanda's main module and the entry point for the program."
from threading import Thread
import components
import config


def build_startup_message():
    """Build the startup string, an announcement sent to newly-connected
users or through newly-initialized drivers."""
    # Is the message enabled?
    if not config.conf['general']['sendmotd']:
        return None
    # Do we have a message of the day?
    if config.conf['general']['motd']:
        startstr = config.conf['general']['motd']
    else:
        startstr = "I am completely operational, and all my circuits are functioning perfectly!"
    # Advertise enabled plugins
    if config.conf['general']['sendmotd'] == 'full':
        for plugin in components.plugins:
            try:
                startstr += " " + plugin.ad
            except AttributeError:
                continue
    return startstr


if __name__ == '__main__':
    # Prepare config
    config.load()
    # Instantiate components
    if components.load():
        print(
            "New plugins and/or drivers have been discovered! Edit the configuration file to enable or customize them."
        )
    # Start all drivers
    if not hasattr(components, 'drivers') or len(components.drivers) < 1:
        raise ValueError("You must configure at least one driver.")
    # Build the startup string
    SS = build_startup_message()
    for driver in components.drivers:
        Thread(target=driver.run).start()
        if SS is not None:
            try:
                driver.announce(SS)
            except AttributeError, NotImplementedError:
                continue
