import dataclasses
from typing import Protocol, TypedDict, runtime_checkable


@runtime_checkable
class Dependency(Protocol):
    parameter_name: str | None = None
    config: dict[str, list[str]]


class Router(Protocol):
    """Middlewares infers automatic"""

    # parent: 'type[Router]'  # Dispatcher if not provided
    # filename: str
    pass


class Handler(Protocol):
    parameters: tuple[int | Dependency, ...]
    router: Router


# class Setup(Protocol):
#     config_type: Literal["env", "ini", "yaml"]
#     register: Literal["decorator", "function"]


class Folder(TypedDict, total=False):
    name: str
    children: "list[Folder]"
    contains: int


@dataclasses.dataclass
class FolderKeys:
    name = "name"
    children = "children"
    contains = "contains"


class Structure(Protocol):
    project_layout: list[Folder]
