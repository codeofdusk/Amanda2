"Amanda's main module and the entry point for the program."
from threading import Thread
import components
import config
import utils

if __name__ == '__main__':
    # Prepare config
    config.load()
    # Instantiate components
    if components.load():
        print(
            "New plugins and/or drivers have been discovered! Edit the configuration file to enable or customize them."
        )
    # Start all drivers
    if not hasattr(components, 'drivers') or len(components.drivers) < 1:
        raise ValueError("You must configure at least one driver.")
    for driver in components.drivers:
        Thread(target=driver.run).start()
        ss=utils.build_startup_message(short=getattr(driver,'short_announcements',False))
        if ss is not None:
            try:
                driver.announce(ss)
            except (AttributeError, NotImplementedError):
                continue
