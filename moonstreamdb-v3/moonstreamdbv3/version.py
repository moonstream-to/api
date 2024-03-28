import os

VERSION = "UNKNOWN"

try:
    PATH = os.path.abspath(os.path.dirname(__file__))
    VERSION_FILE = os.path.join(PATH, "version.txt")
    with open(VERSION_FILE) as ifp:
        VERSION = ifp.read().strip()
except:
    pass
