import skpy
import dateparser
from datetime import datetime
import wolfram
import settings
class MySkype(skpy.SkypeEventLoop):
    def onEvent(self,event):
        if isinstance(event,skpy.SkypeNewMessageEvent) and event.msg.chat.id == settings.window:
            #Get the message
            q=str(event.msg.content)
            #Is this a Wolfram command?
            if hasattr(settings,"wolframkey") and q.startswith("?"):
                event.msg.chat.setTyping(active=True)
                try:
                    return event.msg.chat.sendMsg(wolfram.query(q[1:]))
                except:
                    import traceback
                    return event.msg.chat.sendMsg(traceback.format_exc())
            #Is this a special command?
            if q.startswith("!"):
                #Drop the exclamation point.
                q=q[1:]
                if q == "lifespan":
                    return event.msg.chat.sendMsg("My time of death has been calculated as " + str(s.conn.tokenExpiry['skype']) + ". At that time, my administrator will need to bring me back to life!")
                if q.startswith("expire"):
                    #Split the date string.
                    qt=q.split(" ")
                    if len(qt) < 2:
                        return event.chat.sendMsg("Please specify a time interval!")
                    datestr=' '.join(qt[1:])
                    dateobj=dateparser.parse(datestr)
                    if dateobj == None:
                        return event.msg.chat.sendMsg("Invalid expiration date.")
                    event.msg.chat.sendMsg("Topic set to expire on " + str(dateobj) + ".")
                    self.temp_topic=event.msg.chat.topic
                    self.topic_expiry=dateobj
    def cycle(self):
        skpy.SkypeEventLoop.cycle(self)
        #Known bug: topic expiry doesn't work unless system time is in UTC
        if hasattr(self,'temp_topic') and self.temp_topic != None and hasattr(self,'topic_expiry') and self.topic_expiry != None and self.chats[settings.window].topic == self.temp_topic and datetime.now() > self.topic_expiry:
            if hasattr(settings,'default_topic'):
                self.chats[settings.window].setTopic(settings.default_topic)
            else:
                self.chats[settings.window].setTopic("Hangin' in Suspense")
            self.temp_topic=None
            self.topic_expiry=None

if settings.microsoft:
    raise NotImplementedError
else:
    s=MySkype(settings.skypeuser,settings.skypepass,autoAck=True)
    #build the startup string.
    #Do we have a message of the day?
    if hasattr(settings,"motd"):
        startstr=settings.motd
    else:
        startstr="I Am Completely Operational, And All My Circuits Are Functioning Perfectly!"
    #Do we have Wolfram?
    if hasattr(settings,"wolframkey"):
        startstr+=" Send ? followed by a query to send to Wolfram Alpha."
    #Add message about special commands.
    startstr+=" Prefix special commands with ! (documentation coming soon!)"
    #Send it out.
s.chats[settings.window].sendMsg(startstr)
s.loop()
