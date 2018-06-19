import skpy
from request import request
from drivers.BaseDriver import BaseDriver
import utils

configspec = (
    '[drivers]', '# Skype',
    '# This driver adds support for Skype. It requires skpy from PyPI and a Skype account for sending and receiving messages with users.',
    '[[skype]]', 'enabled = boolean(default = False)',
    '# The Skype username that Amanda should use.',
    'user=string(default=\'\')', '# The Skype user\'s password.',
    'pwd=string(default=\'\')',
    '# If you wish to use skpy\'s credential caching features, specify the tokenfile to use.',
    '# You probably don\'t need to do this unless you are having authentication issues.',
    'tokenFile=string(default=\'\')',
    '# Should this driver automatically acknowledge all incoming Skype events?',
    '# Note: you probably want to leave this enabled unless another client shares this account with Amanda.',
    'autoAck = boolean(default=True)',
    '# What status should Amanda present to other clients?',
    '# The default is to present as online unless a window is set, otherwise present as offline.',
    '# If you wish to always present as online or offline, set this option to online or offline.',
    'status = option(\'default\',\'offline\',\'online\',default=\'default\')',
    '# If this driver should only respond to messages from a certain Skype group chat, enter the cloud identifier of that chat here.',
    'window=string(default=\'\')')


class SkypeDriver(BaseDriver, skpy.SkypeEventLoop):
    def __init__(self,
                 user=None,
                 pwd=None,
                 tokenFile=None,
                 autoAck=True,
                 status="default",
                 window=None):
        "Initialize the user-facing Skype driver."
        if tokenFile == '':
            tokenFile = None
        if window:
            self.window = window
            if status == "default":
                status = None
        else:
            self.window = None
            if status == "default":
                status = skpy.util.SkypeUtils.Status.Online
        if status == "online":
            status = skpy.util.SkypeUtils.Status.Online
        elif status == "offline":
            status = skpy.util.SkypeUtils.Status.Offline
        super().__init__(
            user=user,
            pwd=pwd,
            tokenFile=tokenFile,
            autoAck=autoAck,
            status=status)

    def onEvent(self, event):
        if isinstance(event, skpy.SkypeNewMessageEvent) and (
                not self.window or event.msg.chat.id == self.window):
            # Get the message
            q = str(event.msg.content)
            request(q, driver=self, event=event)

    # Implement the Amanda driver interface.

    def working(self, state, request, *args, **kwargs):
        if 'event' in request.kwargs:
            request.kwargs['event'].msg.chat.setTyping(active=state)

    def say(self, msg, request=None, *args, **kwargs):
        if hasattr(request, 'kwargs') and 'event' in request.kwargs:
            request.kwargs['event'].msg.chat.sendMsg(msg)
        elif self.window:
            self.chats[self.window].sendMsg(msg)
        else:
            print(
                "Warning! Skype message destined for nowhere. Please set a window if you wish to use this plugin: "
                + msg)

    def announce(self, msg):
        if self.window:
            return self.say(msg, request=None)
        else:
            self.setMood(msg)

    def run(self):
        return self.loop()
