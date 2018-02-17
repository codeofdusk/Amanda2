import skpy
import dateparser
from datetime import datetime
import wolfram
import geo
import settings
class MySkype(skpy.SkypeEventLoop):
    def onEvent(self,event):
        if isinstance(event,skpy.SkypeNewMessageEvent) and event.msg.chat.id == settings.window:
            #Get the message
            q=str(event.msg.content)
            try:
                # First attempt to call plugin explicitly
                if hasattr(settings,'allow_explicit') and settings.allow_explicit and q.startswith("!"):
                    # Get the plugin name and args
                    qt=q[1:].split(" ")
                    pn=qt[0]
                    pa=' '.join(qt[1:])
                    # Search for the plugin
                    for plugin in settings.plugins:
                        if hasattr(plugin,'name') and plugin.name == pn:
                            event.msg.chat.setTyping(active=True)
                            return event.msg.chat.sendMsg(plugin.run(pa,explicit=True))
                    return event.msg.chat.sendMsg("Invalid command.")
                # Attempt to call plugin implicitly
                if hasattr(settings,'allow_implicit') and settings.allow_implicit:
                    for plugin in settings.plugins:
                        if hasattr(plugin,'match'):
                            m = plugin.match(q)
                            if m:
                                event.msg.chat.setTyping(active=True)
                                return event.msg.chat.sendMsg(plugin.run(m))
            except:
                import traceback
                return event.msg.chat.sendMsg(traceback.format_exc())

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
