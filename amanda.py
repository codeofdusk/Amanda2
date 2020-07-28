"""Amanda's main module and the entry point for the program.
Copyright 2018–2020 Bill Dengler <codeofdusk@gmail.com>. Licensed under MIT."""

import atexit
import os

from threading import Thread
import components
import config
import utils


def cleanup():
    try:
        os.remove("amanda.pid")
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    if os.path.exists("amanda.pid"):
        raise Exception("Amanda is already running!")
    else:
        with open("amanda.pid", "w") as pidfile:
            pidfile.write(str(os.getpid()))
        atexit.register(cleanup)
    print(
        "Amanda: a simple, extensible chatbot framework.\nCopyright 2018–2020 Bill Dengler <codeofdusk@gmail.com>. Licensed under MIT."
    )

    # Prepare config
    config.load()

    # Instantiate components
    if components.load():
        print(
            "New plugins and/or drivers have been discovered! Edit the configuration file to enable or customize them."
        )

    # Start all drivers
    threads = []
    if not hasattr(components, "drivers") or len(components.drivers) < 1:
        raise Exception("You must configure at least one driver.")
    for driver in components.drivers:
        tr = Thread(target=driver.run)
        threads.append(tr)
        tr.daemon = True
        tr.start()
        short = config.conf["general"]["sendmotd"] == "retracted" or getattr(
            driver, "short_announcements", False
        )
        ss = utils.build_startup_message(short=short)
        if ss is not None:
            try:
                driver.announce(ss)
            except (AttributeError, NotImplementedError):
                continue

    for tr in threads:
        tr.join()
