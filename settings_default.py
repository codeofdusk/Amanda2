#Amanda settings file
#Before using Amanda, fill in these settings, then copy this file to settings.py.
# Imports.
# If you wish to use the geolocation plugin, you will need to install the requests package from PyPI. Once installed, uncomment the following line as well as the line in the plugins section.
#from plugins import geo
# If you wish to use Wolfram Alpha, you will need to install the wolframalpha package from PyPI and obtain an API key. Once you have a key and have installed the required package, uncomment this line and the one in the plugins section, then add your API key where required.
#from plugins import wolframalpha
#General settings
#Message Of The Day
#If Amanda should send a custom message on startup, uncomment the following line and specify your message. Leave commented to send the default message.
#motd=""
#Custom Huh Messages
#Uncomment and supply a random list of messages to send when Amanda doesn't understand a message.
#huh_messages=[]
# Plugin advertisement
# Enter the names of plugins to advertise into the below list, leave empty to advertise all, or comment out to disable advertisement.
advertise_plugins=[]
#Skype settings
#Does Amanda log into Skype using a Microsoft account?
microsoft=False
#Amanda's Skype name/Microsoft account email
skypeuser=""
#Amanda's Skype/Microsoft password
skypepass=""
#Skype cloud identifier of the window where Amanda resides.
window=""

# Plugins
# Plugins add functionality to Amanda. They can be enabled and configured here.
plugins=[
# Uncomment the below line to enable the IP geolocation plugin.
#geo.GeolocationPlugin()
# Uncomment the below line and add your API key between the quotation marks to enable Wolfram Alpha.
#wolfram.WolframAlphaPlugin("")
]

# Advanced options
# Explicit plugin use
# Comment out (or set to False) the following line to disable the ability to call plugins explicitly (entering !pluginname args to use an enabled plugin). Disabling this feature may be useful in special circumstances but it should generally be left enabled.
allow_explicit=True
# Implicit plugin use
# Comment out (or set to False) the following line to disable the ability to call plugins implicitly (using custom match patterns). Disabling this feature may be useful in special circumstances but it should generally be left enabled.
allow_implicit=True
