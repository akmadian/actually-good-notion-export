from .Page import Page
from typing import List, Optional

import os
import json
import shutil

class Export:
    def __init__(self, inpath: str, outpath: Optional[str] = None):
        self.inpath = inpath
        self.outpath = outpath if outpath else f"{inpath}-actually-good"
        self.pages: List[Page] = []
        self.replacements = self.__load_replacements()

        self.__ingest_export()

    def __ingest_export(self):
        print(self.inpath)
        for root, _, files in os.walk(self.inpath, topdown=True):
            for name in files:
                if name.endswith(".html"):
                    fullname = os.path.join(root, name)
                    print(fullname)
                    self.pages.append(Page(fullname))

    def __replicate_dir_structure(self):
        for root, _, _ in os.walk(self.inpath):
            structure = os.path.join(self.outpath, root[len(self.inpath):])
            if not os.path.isdir(structure):
                os.mkdir(structure)

    def __load_replacements(self):
        with open("notion/replacements.json", 'r') as f:
            return json.loads(f.read())

    def __remove_old_dir(self):
        try:
            shutil.rmtree(self.outpath)
        except FileNotFoundError as e:
            pass

    def do_replacements(self):
        for page in self.pages:
            page.do_replacements(self.replacements)

    def do_export(self):
        self.__remove_old_dir()
        self.__replicate_dir_structure()

        for page in self.pages:
            new_path = f'{self.outpath}/{page.name}'
            with open(new_path, 'w+') as f:
                f.write(page.contents)