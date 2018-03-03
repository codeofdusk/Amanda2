import os,imp
import skpy
imp.load_source('request', os.path.join(os.path.dirname(__file__), '../request.py'))
from request import request
class SkypeDriver(skpy.SkypeEventLoop):
    def __init__(self, user=None, pwd=None, tokenFile=None, autoAck=True, status=None, window=None):
        "Initialize the user-facing Skype driver."
        # Initialize the internal-use (real) Skype driver
        self._driver=_driver(self)
        if window:
            # We have a window
            self.window=window
        super().__init__(user=user, pwd=pwd, tokenFile=tokenFile, autoAck=autoAck, status=status)
    def onEvent(self,event):
        if isinstance(event,skpy.SkypeNewMessageEvent) and (not self.window or event.msg.chat.id == self.window):
            #Get the message
            q=str(event.msg.content)
            request(q,driver=self._driver,event=event)
    # Implement the Amanda driver interface.
    def run(self):
        return self.loop()
    def announce(self,*args,**kwargs):
        return self._driver.announce(*args,**kwargs)
    def say(self,*args,**kwargs):
        return self._driver.say(*args,**kwargs)
    def working(self,*args,**kwargs):
        return self._driver.working(*args,**kwargs)

class _driver(object):
    "Driver object for internal use."
    def __init__(self,skype):
        self._skype=skype
    def working(self,state,request,*args,**kwargs):
        if 'event' in request.kwargs:
            request.kwargs['event'].msg.chat.setTyping(active=state)
    def say(self,msg,request=None,*args,**kwargs):
        if hasattr(request,'kwargs') and 'event' in request.kwargs:
            request.kwargs['event'].msg.chat.sendMsg(msg)
        elif hasattr(self._skype,'window'):
            self._skype.chats[self._skype.window].sendMsg(msg)
        else:
            print("Warning! Skype message destined for nowhere. Please set a window if you wish to use this plugin: " + msg)
    def announce(self,*args,**kwargs):
        #For now
        return self.say(*args,**kwargs)
