from .BasePlugin import BasePlugin
import wolframalpha


class WolframAlphaPlugin(BasePlugin):
    name="wolfram"
    ad="Type a question mark followed by a query to send to Wolfram Alpha, or !wolfram <query> to send a request and see what Wolfram Alpha thought you said."
    def run(self,command,explicit=False,*args,**kwargs):
        "Send a query to Wolfram Alpha."
        q=self.client.query(command,units="metric")
        #Check for invalid input.
        if not hasattr(q,'pods'):
            return False
        #response string
        resp=""
        #Filter Wolfram results and populate response string.
        for pod in q.pods:
            if explicit or ("input" not in pod.title.lower() and pod.text != None):
                if explicit or (pod.title.lower() != "result" and pod.title.lower() != "response"):
                    resp += str(pod.title) + "\n"
                resp+=str(pod.text) + "\n"
        return resp
    def __init__(self,key):
        self.client=wolframalpha.Client(key)
    def match(self,s):
        return s[1:] if s.startswith("?") else False
