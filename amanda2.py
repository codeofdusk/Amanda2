from request import request
from threading import Thread
import settings

def build_startup_message():
    #build the startup string.
    #Do we have a message of the day?
    if hasattr(settings,"motd"):
        startstr=settings.motd
    else:
        startstr="I Am Completely Operational, And All My Circuits Are Functioning Perfectly!"
    # Advertise enabled plugins
    if hasattr(settings,'advertise_plugins'):
        for plugin in settings.plugins:
            if plugin.name in settings.advertise_plugins or len(settings.advertise_plugins) < 1:
                if hasattr(plugin,'ad'):
                    startstr+=" " + plugin.ad
    return startstr

if __name__ == '__main__':
    # Start all drivers
    if not hasattr(settings,'drivers') or len(settings.drivers) < 1:
        raise ValueError("You must configure at least one driver.")
    # Build the startup string
    ss=build_startup_message()
    for driver in settings.drivers:
        Thread(target=driver.run).start()
        if hasattr(driver,'announce'):
            driver.announce(ss)
        else:
            driver.say(ss,request=None)
