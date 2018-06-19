"Module containing utility functions that don't belong anywhere else."

import config
import components


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
