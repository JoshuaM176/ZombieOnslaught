import json
from os import path, curdir, listdir
from copy import deepcopy

ROOT = path.abspath(curdir)

class ResourceLoader:

    def __init__(self, resource: str, location: str):
        self.resources = {}
        self.rPath = path.join(ROOT, 'resources', location, resource)
        self.files = listdir(self.rPath)

    def load(self, path: path):
        with open(path, 'r') as f:
            data = json.load(f)
        for key, value in data.items():
            self.resources[key] = value

    def load_all(self):
        for file in self.files:
            self.load(path.join(self.rPath, file))

    def update(self, data: dict, new_data: dict):
        for key, value in new_data.items():
            if type(data[key]) == dict and new_data.get(key) is not None:
                self.update(data[key], new_data[key])
            else:
                data[key] = value
        return data

    def get(self, name: str):
        return deepcopy(self.resources[name])