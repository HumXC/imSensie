import time

import shiroko

import ba
from ba import screenshot
from ba.utils import *

ADDR: str = "192.168.1.17:15600"


def main():
    srk = shiroko.Client(ADDR)
    screenshot.Init(srk)
    screenshot.Get().Save("screenshot-" + str(time.time()) + ".png")
    time.sleep(3)
    print("PP")


if __name__ == "__main__":
    main()
