# Amanda configuration
# Before using Amanda, edit the below settings.

[general]
# Should Amanda send a message on startup?
# Set to None to send no message, brief to send a message without usage details for installed plugins, or full to send a message including plugin advertisements.
# Note: the brief option is recommended for protocols where message length is limited (Skype with no window specified, etc). Full is recommended otherwise, unless a large number of plugins is enabled.
sendmotd=option(None,'brief','full',default='brief')
# The text of the message to send when Amanda starts. If not set, the default text will be used.
motd=string(default=None)
# Huh messages
# If set, Amanda will randomly select a message from this list when it doesn't understand a request. For example:
#huh_messages="Huh?","I don't understand.","I didn't get that."
huh_messages=list(default=None)

# Drivers
# Drivers allow Amanda to communicate with users.
# This can be via IM systems, such as Skype, or through almost any other channel.
# You may use the included drivers, write new ones in a few lines of Python, or copy those written by others to the drivers directory.
# If you write a new driver, I encourage you to contribute it back as a pull request so that others can use it as well.
# Each driver section contains a special enabled option. When set to True, the driver is fully launched and prepared for user requests when Amanda starts.
# While disabled drivers cannot receive user requests, some code in every driver is run on launch. Therefore, you should only place drivers you trust into the drivers directory.
[drivers]

# Plugins
# Plugins give Amanda functionality, such as returning Wolfram Alpha results or geolocating IP addresses.
# You may use the included plugins, write new ones in a few lines of Python, or copy those written by others to the plugins directory.
# If you write a new plugin, I encourage you to contribute it back as a pull request so that others can use it as well.
# Each plugin section contains a special enabled option. When set to True, the plugin is fully initialized and will be used when processing user requests.
# While disabled plugins are not consulted when processing messages from users, some code in every plugin is run on launch. Therefore, you should only place plugins you trust into the plugins directory.
[plugins]


[advanced]
# Explicit plugin use
# Set the following option to False to disable the ability to call plugins explicitly (entering !pluginname args to use an enabled plugin). Disabling this feature may be useful in special circumstances but it should generally be left enabled.
allow_explicit=boolean(default=True)
# Implicit plugin use
# Set the following option to False to disable the ability to call plugins implicitly (using custom match patterns). Disabling this feature may be useful in special circumstances but it should generally be left enabled.
allow_implicit=boolean(default=True)
