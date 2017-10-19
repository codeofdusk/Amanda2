import skpy
import dateparser
from datetime import datetime
import wolfram
import settings
class MySkype(skpy.SkypeEventLoop):
    def onEvent(self,event):
        if isinstance(event,skpy.SkypeNewMessageEvent):
            print("New message from " + event.msg.chat.id + ": " + event.msg.content)

if settings.microsoft:
    raise NotImplementedError
else:
    s=MySkype(settings.skypeuser,settings.skypepass,autoAck=True)
print("Ready to discover windows...")
s.loop()
