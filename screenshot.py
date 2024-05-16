import time

from shiroko import Client

from main import ADDR

if __name__ == "__main__":
    srk = Client(ADDR)
    srk.input.Wakeup()
    size = srk.window.GetSize()
    srk.window.SetSize(1080, 1920)
    time.sleep(0.5)
    png = srk.screencap.Png()
    srk.window.ResetSize()
    with open("screenshot/" + str(time.time()) + ".png", "wb") as f:
        f.write(png)
