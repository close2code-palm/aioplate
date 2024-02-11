from aioplate.initial.entities import FolderKeys, Structure
from aioplate.initial.framework import MIDDLEWARES, ROUTERS


class IntroBotPlate(Structure):
    """Default layout."""

    project_layout = [
        {FolderKeys.name: "routers", FolderKeys.contains: ROUTERS},
        {FolderKeys.name: "middlewares", FolderKeys.contains: MIDDLEWARES},
        {FolderKeys.name: "keyboards"},
        {
            FolderKeys.name: "infra",
            FolderKeys.children: [
                {FolderKeys.name: "database"},
            ],
        },
        {FolderKeys.name: "states"},
    ]


# class ProSetup(Setup):
#     config_type = "env"
#     register = "decorator"


# TOKEN_CONFIG = {"tg": {"str": ["TOKEN"]}}
