"Module containing utility functions that don't belong anywhere else."

import config
import components


def build_startup_message(short=False):
    """Build the startup string, an announcement sent to newly-connected
users or through newly-initialized drivers.
The short parameter controls if full plugin advertisements are sent as part of the message based on driver support."""
    # Is the message enabled?
    if not config.conf['general']['sendmotd']:
        return None
    # Do we have a message of the day?
    if config.conf['general']['motd']:
        startstr = config.conf['general']['motd']
    else:
        startstr = "I am completely operational, and all my circuits are functioning perfectly!"
    # Advertise enabled plugins if needed
    if config.conf['general']['sendmotd'] == 'full' and not short:
        startstr += build_plugin_ad()
    elif short:
        startstr+=" Send !help (an exclamation point followed by the word help) for a complete list of my features!"
    return startstr


def build_plugin_ad():
    "Advertise enabled plugins for use in help texts and motd."
    res = ""
    for plugin in components.plugins:
        try:
            res += " " + plugin.ad
        except AttributeError:
            continue
    return res


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
