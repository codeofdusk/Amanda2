#Amanda's Wolfram Alpha support, separated into its own module.
import wolframalpha
import settings
def query(command):
    "Send a query to Wolfram Alpha."
    #Is Wolfram enabled?
    if hasattr(settings,"wolframkey"):
        w=wolframalpha.Client(settings.wolframkey)
    else:
        return "My Wolfram Alpha module has been disabled. If you want to use it, tell my administrator to uncomment wolframkey in settings.py and set my Wolfram Alpha app ID."
    #Wolfram Alpha query
    q=w.query(command,units="metric")
    #Check for invalid input.
    if not hasattr(q,'pods'):
        #Respond with a user-supplied huh message if available
        if hasattr(settings,"huh_messages"):
            import random
            return random.choice(settings.huh_messages)
        else:
            return "Huh?"
    #response string
    resp=""
    #Filter Wolfram results and populate response string.
    for pod in q.pods:
        if "input" not in pod.title.lower() and pod.text != None:
           if pod.title.lower() != "result" and pod.title.lower() != "response":
                resp += pod.title + "\n"
           resp+=pod.text + "\n"
    return resp
