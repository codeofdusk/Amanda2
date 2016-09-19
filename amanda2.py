import skpy
import wolfram
import settings
class MySkype(skpy.SkypeEventLoop):
    def onEvent(self,event):
        if isinstance(event,skpy.SkypeNewMessageEvent) and event.msg.chat.id == settings.window:
            #Get the message
            q=event.msg.content
            #Is this a Wolfram command?
            if hasattr(settings,wolframkey) and str(q).startswith("?"):
                event.msg.chat.setTyping(active=True)
                try:
                    return event.msg.chat.sendMsg(wolfram.query(q[1:]))
                except:
                    return event.msg.chat.sendMsg("\"Huh?\" - Ashleah Chamberlain")
            #Is this a special command?

if settings.microsoft:
    raise NotImplementedError
else:
    s=MySkype(settings.skypeuser,settings.skypepass,autoAck=True)
    #build the startup string.
    #Do we have a message of the day?
    if hasattr(settings,motd):
        startstr=settings.motd
    else:
        startstr="I Am Completely Operational, And All My Circuits Are Functioning Perfectly!"
    #Do we have Wolfram?
    if hasattr(settings,wolframkey):
        startstr+=" Send ? followed by a query to send to Wolfram Alpha."
    #Send it out.
s.chats[settings.window].sendMsg(startstr)
s.loop()
