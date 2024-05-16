import os
from .cv import Image

All: dict[str, Image] = {}


def get(name: str) -> Image:
    return All[name].Copy()


def release():
    All.clear()


def __init():
    files = []
    dirName = os.path.join(os.path.dirname(__file__), "images")
    for file in os.listdir(dirName):
        if file.endswith(".png"):
            files.append(file[:-4])
    for file in files:
        with open(os.path.join(dirName, file + ".png"), "rb") as f:
            All[file] = Image(f.read())


__init()
