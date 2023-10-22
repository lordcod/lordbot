import pathlib
import sys

def inimport(name):
    _parentdir = pathlib.Path(__file__).parent.parent.resolve()
    sys.path.insert(0, str(_parentdir))
    libbery = __import__(name) 
    sys.path.remove(str(_parentdir))
    return libbery