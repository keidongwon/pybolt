import os
import sys
from collections import OrderedDict
import json


class FileBase:
    def __init__(self):
        self.values = dict()

    def load(self, filename, path=None):
        self.values.clear()
        if path is None:
            path = os.getcwd() + "/data"
        path += "/%s.json" % os.path.splitext(filename)[0]
        
        try:
            with open(path, "r") as _file:
                self.values = json.loads(_file.read(), object_pairs_hook=OrderedDict)
        except IOError as ioe:
            raise

    def get(self, key1, key2=None):
        try:
            if key2 is None:
                return self.values[key1]
            return self.values[key1][key2]
        except:
            return None
