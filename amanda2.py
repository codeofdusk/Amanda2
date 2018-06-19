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
    # Build the startup string
    SS = utils.build_startup_message()
    for driver in components.drivers:
        Thread(target=driver.run).start()
        if SS is not None:
            try:
                driver.announce(SS)
            except (AttributeError, NotImplementedError):
                continue
