import os
from contextlib import suppress

from aioplate.entities import Folder
from aioplate.generator.constructor import StructureGenerator


def make_folder(path: str):
    with suppress(FileExistsError):
        os.makedirs(path)


def _make_package(path: str):
    make_folder(path)
    with open(path + "/__init__.py", "w+") as f:
        f.write("\n")


class FSStructureGenerator(StructureGenerator):
    def __init__(self, structure: list[Folder], project: str, src: bool = True):
        self.src = src
        self.project = project
        self.structure = structure

    def generate_structure(self):
        prefix = f"/{self.project}"
        if self.src:
            make_folder("./src")
            prefix = "/src" + prefix
        prefix = "." + prefix
        _make_package(prefix)
        self._generate_structure_unit(prefix, self.structure)

    def _generate_structure_unit(self, prefix: str, structure: list[Folder]):
        for folder in structure:
            folder_relative = f'{prefix}/{folder["name"]}'
            _make_package(folder_relative)
            if "children" in folder:
                self._generate_structure_unit(folder_relative, folder["children"])
