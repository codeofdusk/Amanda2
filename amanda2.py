import skpy
import settings
import random

class request(object):
    def __init__(self,content,driver=None,*args,**kwargs):
        "Take a string and return a response (if available) or False for no response."
        self.content=content
        self.driver=driver
        self.accepted=False
        self.response=None
        try:
            # First attempt to call plugin explicitly
            if hasattr(settings,'allow_explicit') and settings.allow_explicit and self.content.startswith("!"):
                self.accept()
                # Get the plugin name and args
                qt=self.content[1:].split(" ")
                pn=qt[0]
                pa=' '.join(qt[1:])
                # Search for the plugin
                for plugin in settings.plugins:
                    if hasattr(plugin,'name') and plugin.name.lower() == pn.lower():
                        self.response = plugin.run(pa,explicit=True)
            # Attempt to call plugin implicitly
            if hasattr(settings,'allow_implicit') and settings.allow_implicit:
                for plugin in settings.plugins:
                    if hasattr(plugin,'match'):
                        m = plugin.match(self.content)
                        if m:
                            self.accept()
                            self.response = plugin.run(m)
        except:
            import traceback
            self.response = traceback.format_exc()
        finally:
            self.finalize()
    def __str__(self):
        if not self.response:
            # do we have huh messages?
            if hasattr(settings,'huh_messages'):
                self.response = random.choice(settings.huh_messages)
            else:
                self.response = "I don't understand."
        return self.response
    def accept(self):
        if hasattr(self.driver,'working'):
            self.driver.working(True,request=self)
        self.accepted=True
    def finalize(self):
        if hasattr(self.driver,'say'):
            self.driver.say(str(self),request=self)
        if hasattr(self.driver,'working'):
            self.driver.working(False,request=self)
class MySkype(skpy.SkypeEventLoop):
    def onEvent(self,event):
        if isinstance(event,skpy.SkypeNewMessageEvent) and event.msg.chat.id == settings.window:
            #Get the message
            q=str(event.msg.content)
            r=request(q)
            if r.accepted:
                return event.msg.chat.sendMsg(str(r))

if __name__ == '__main__':
    if settings.microsoft:
        raise NotImplementedError
    s=MySkype(settings.skypeuser,settings.skypepass,autoAck=True)
    #build the startup string.
    #Do we have a message of the day?
    if hasattr(settings,"motd"):
        startstr=settings.motd
    else:
        startstr="I Am Completely Operational, And All My Circuits Are Functioning Perfectly!"
    # Advertise enabled plugins
    if hasattr(settings,'advertise_plugins') and settings.advertise_plugins:
        for plugin in settings.plugins:
            if hasattr(plugin,'ad'):
                startstr+=" " + plugin.ad
        #Send it out.
        s.chats[settings.window].sendMsg(startstr.strip())
        s.loop()
