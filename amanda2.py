"Amanda's main module and the entry point for the program."
from threading import Thread
import settings
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
        for plugin in settings.plugins:
            if hasattr(plugin, 'ad'):
                startstr += " " + plugin.ad
    return startstr


if __name__ == '__main__':
    # Prepare config
    config.load()
    # Start all drivers
    if not hasattr(settings, 'drivers') or len(settings.drivers) < 1:
        raise ValueError("You must configure at least one driver.")
    # Build the startup string
    SS = build_startup_message()
    for driver in settings.drivers:
        Thread(target=driver.run).start()
        if hasattr(driver, 'announce') and SS is not None:
            driver.announce(SS)
