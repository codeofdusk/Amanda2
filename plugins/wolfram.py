"""Contains a plugin for retrieving results from the Wolfram Alpha knowledge engine using the wolframalpha package.
Copyright 2018 - Bill Dengler <codeofdusk@gmail.com>. Licensed under MIT."""


from plugins.BasePlugin import BasePlugin
import wolframalpha

configspec = (
    "[plugins]", "# Wolfram Alpha",
    "# This plugin returns responses from the Wolfram Alpha knowledge engine.",
    "# The wolframalpha package from PyPI and a Wolfram Alpha API key are required.",
    "[[wolfram]]", "enabled=boolean(default=False)", "key=string(default='')")


class WolframAlphaPlugin(BasePlugin):
    invocations = ("wolfram", )
    ad = "Type a question mark followed by a query to send to Wolfram Alpha, or !wolfram <query> to send a request and see what Wolfram Alpha thought you said."

    def run(self, r):
        "Send a query to Wolfram Alpha."
        if not r.content:
            return self.ad
        q = self.client.query(r.content, units="metric")
        # Check for invalid input.
        if not hasattr(q, 'pods'):
            return False
        # response string
        resp = ""
        # Filter Wolfram results and populate response string.
        for pod in q.pods:
            if r.invocation is not None or (
                    hasattr(pod, 'title') and "input" not in pod.title.lower()
                    and hasattr(pod, 'text') and pod.text is not None):
                if r.invocation is not None or (
                        pod.title.lower() != "result"
                        and pod.title.lower() != "response"):
                    resp += str(pod.title) + "\n"
                resp += str(pod.text) + "\n"
        return resp

    def __init__(self, key):
        self.client = wolframalpha.Client(key)

    def match(self, s):
        return s[1:] if s.startswith("?") else False
