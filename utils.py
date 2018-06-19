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


def saypager(n):
    """A decorator to split large messages into pages of n characters, for drivers with maximum character limits. May be useful for future drivers/contributors.
        Use it by decorating your say method like:
        @saypager(n)
        where n is the maximum message size for your protocol."""

    def decorator(say):
        def f(self, msg, request=None, *args, **kwargs):
            for i in range(0, len(msg), n):
                say(self, msg=msg[i:i + n], request=request, *args, **kwargs)

        return f

    return decorator
