from .Page import Page
from typing import List, Optional

import os

class Export:
    def __init__(self, inpath: str, outpath: Optional[str] = None):
        self.inpath = inpath
        self.outpath = outpath if outpath else f"./{inpath}-actually-good"
        self.pages: List[Page] = []

        #self.__replicate_dir_structure()
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