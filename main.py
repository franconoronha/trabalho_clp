import ctypes
import os

dirname = os.getcwd()
if os.name == "nt":
    suffix = ".dll"
else:
    suffix = ".so"

path = dirname + "\\shared" + suffix
shared = ctypes.CDLL(path)

print(shared.soma(10, 20))