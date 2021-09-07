import ctypes
import pathlib
import inspect
import os

script_path = inspect.getframeinfo(inspect.currentframe()).filename
dir_of_script = os.path.dirname(os.path.abspath(script_path))
lib = ctypes.CDLL(dir_of_script + "/libcryptool.so")


def encrypt(target, source, password):
    result = -1
    try:
        result = lib.encrypt(bytes(target, encoding="ascii"),
                             bytes(source, encoding="ascii"), bytes(password, encoding="ascii"))
        if result != 0:
            f = pathlib.Path(target)
            f.unlink()
        return result
    except:
        return result


def decrypt(target, source, password):
    result = -1
    try:
        result = lib.decrypt(bytes(target, encoding="ascii"),
                             bytes(source, encoding="ascii"), bytes(password, encoding="ascii"))
        if result != 0:
            f = pathlib.Path(target)
            f.unlink()
        return result
    except:
        return result
