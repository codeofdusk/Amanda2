#Amanda settings file
#Before using Amanda, fill in these settings, then copy this file to settings.py.
#General settings
#Message Of The Day
#If Amanda should send a custom message on startup, uncomment the following line and specify your message. Leave commented to send the default message.
#motd=""
#Custom Huh Messages
#Uncomment and supply a random list of messages to send when Amanda doesn't understand a message.
#huh_messages=[]
# Plugin advertisement
# Comment out (or set to false) the following line to disable advertisement of enabled plugins (using text supplied with each plugin) when Amanda starts. If you have enabled a large number of plugins, disabling this advertisement may be a good idea to avoid sending a large message on startup.
advertise_plugins=True
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

]

# Advanced options
# Explicit plugin use
# Comment out (or set to False) the following line to disable the ability to call plugins explicitly (entering !pluginname args to use an enabled plugin). Disabling this feature may be useful in special circumstances but it should generally be left enabled.
allow_explicit=True
# Implicit plugin use
# Comment out (or set to False) the following line to disable the ability to call plugins implicitly (using custom match patterns). Disabling this feature may be useful in special circumstances but it should generally be left enabled.
allow_implicit=True
