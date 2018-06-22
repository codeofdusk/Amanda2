# Amanda
Amanda is a simple, extensible chatbot framework written in Python. At the moment, it supports the retrieval of responses from [Wolfram Alpha](http://wolframalpha.com) and the [freegeoip.net](http://freegeoip.net) API for Skype users, but new features and protocol support can be added easily in the form of plugins and drivers respectively.

## Usage
To start Amanda, pass amanda.py as an argument to the python3 interpreter on your system. For example, from the root of this repository:

    python3 amanda.py

or, on some (newer) systems:

    python amanda.py

Once Amanda is started for the first time, a configuration file is generated at `amanda.conf`. Open it in your text editor and fill in your settings, then re-run Amanda when finished.

### Systemd support
If, like most modern Gnu/Linux distributions, your system uses Systemd for service management, a systemd service generation script is available for your convenience. To use it, run `systemd.sh` in this repository as a non-root user. Then, you can:

    systemd enable amanda # Run Amanda on system start.
    systemd start amanda # Start Amanda as a system service.
## Extensibility
If you wish to extend Amanda's functionality, see the included plugins and drivers as examples. Be sure that your new component inherits from either `BasePlugin` or `BaseDriver` to be discovered by Amanda's configuration system.

If you wish to install a component written by another developer, simply copy its source file (whose name ends in `.py`) to the plugins or drivers directory, then restart Amanda.

I'm sure there's a better way to do some of this; pull requests are greatly appreciated!
