# Amanda configuration
# Before using Amanda, edit the below settings.

[general]
# Should Amanda send a message on startup?
# Set to off to send no message, brief to send a message without usage details for installed plugins, or full to send a message including plugin advertisements.
# Note: the brief option is recommended for protocols where message length is limited (Skype with no window specified, etc). Full is recommended otherwise, unless a large number of plugins is enabled.
sendmotd=option('off','brief','full',default='brief')
# The text of the message to send when Amanda starts. If not set, the default text will be used.
motd=string(default=None)
# Huh messages
# If set, Amanda will randomly select a message from this list when it doesn't understand a request. For example:
#huh_messages="Huh?","I don't understand.","I didn't get that."
huh_messages=list(default=None)

[advanced]
# Explicit plugin use
# Set the following option to False to disable the ability to call plugins explicitly (entering !pluginname args to use an enabled plugin). Disabling this feature may be useful in special circumstances but it should generally be left enabled.
allow_explicit=boolean(default=True)
# Implicit plugin use
# Set the following option to False to disable the ability to call plugins implicitly (using custom match patterns). Disabling this feature may be useful in special circumstances but it should generally be left enabled.
allow_implicit=boolean(default=True)
