"Contains the Request class."
import random
import components
import config
import utils


class request(object):
    "Contains attributes for handling user requests and returning responses. Instantiate this class to make a request."

    def __init__(self, message, driver=None, *args, **kwargs):
        "Take a string and return a response (if available) or False for no response."
        self._message = message
        self.driver = driver
        self.accepted = False
        self.response = None
        self.content = None
        self.invocation = None
        # Expose extra args
        self.args = args
        self.kwargs = kwargs
        try:
            # First attempt to call plugin explicitly
            if config.conf['advanced']['allow_explicit'] and self._message.startswith(
                    "!"):
                self.accept()
                # Get the plugin name and args
                qt = self._message[1:].split(" ")
                self.invocation = qt[0]
                self.content = ' '.join(qt[1:])
                # Is the user requesting the full motd?
                # Note: if we need to implement another special command like this that's a core function, we should create a CorePlugin object that's always loaded and not part of the config that contains these commands.
                try:
                    sendmotd = config.conf['general']['sendmotd']
                    if sendmotd == 'full' and self.driver.short_announcements and self.invocation == "help":
                        self.response = utils.build_plugin_ad()
                except AttributeError:
                    pass
                # Search for the plugin
                for plugin in components.plugins:
                    try:
                        if self.invocation.lower() in plugin.invocations:
                            self.response = plugin.run(self)
                    except AttributeError:
                        continue
            # Attempt to call plugin implicitly
            if config.conf['advanced']['allow_implicit'] and not self._message.startswith(
                    "!"):
                for plugin in components.plugins:
                    try:
                        self.content = plugin.match(self._message)
                    except (AttributeError, NotImplementedError):
                        continue
                    else:
                        if self.content:
                            self.accept()
                            self.response = plugin.run(self)
        except BaseException:
            import traceback
            self.response = traceback.format_exc()
        finally:
            self.finalize()

    def __str__(self):
        if not self.response:
            # do we have huh messages?
            if config.conf['general']['huh_messages']:
                self.response = random.choice(
                    config.conf['general']['huh_messages'])
            else:
                self.response = "I don't understand."
        return self.response

    def accept(self):
        try:
            self.driver.working(True, request=self)
        except (AttributeError, NotImplementedError):
            pass
        self.accepted = True

    def finalize(self):
        if self.accepted:
            try:
                self.driver.say(str(self), request=self)
            except (AttributeError, NotImplementedError):
                pass
            try:
                self.driver.working(False, request=self)
            except (AttributeError, NotImplementedError):
                pass
