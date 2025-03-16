import json
from os import path, curdir, listdir

ROOT = path.abspath(curdir)

class ResourceLoader:

    def __init__(self, resource: str):
        self.resources = {}
        self.rPath = path.join(ROOT, 'resources', 'attributes', resource)
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
        for key, value in new_data:
            data[key] = value

    def get(self, name: str):
        return self.resources[name]