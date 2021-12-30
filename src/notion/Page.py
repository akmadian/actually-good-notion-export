import re
import json

class Page:
    def __init__(self, path: str):
        self.path = path
        self.contents = self.__get_contents()

    def __get_contents(self):
        with open(self.path, 'r') as f:
            return f.read()

    

    