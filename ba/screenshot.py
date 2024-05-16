SCREEN_SIZE = (1080, 1920)
IMAGE_SIZE = (1920, 1080)
import queue
import threading
import time
from typing import cast

from shiroko import Client

from ba.cv import Image


class NoneImageError(Exception):
    """
    Raised when an image is requested, but none is available.
    """


__cur: Image | None = None

__error: Exception | None = None


def Init(srk: Client, interval: float = 0):
    def target():
        global __error, __cur
        while True:
            try:
                __cur = Image(srk.screencap.Png())
                time.sleep(interval)
            except Exception as e:
                __error = e
                return

    threading.Thread(target=target, name="screenshot", daemon=True).start()

    while True:
        try:
            if Get():
                break
        except NoneImageError:
            pass
        time.sleep(0.1)


def Get() -> Image:
    global __error
    if __error:
        raise __error
    if not __cur:
        raise NoneImageError("No image is available.")
    return cast(Image, __cur)
