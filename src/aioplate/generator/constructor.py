import abc
from contextlib import suppress
from dataclasses import dataclass, field
from typing import Protocol

from aioplate.defaults import IntroBotPlate
from aioplate.entities import Structure
from aioplate.exceptions import InvalidHandler
from aioplate.framework import CALLBACK, INLINE, MESSAGE
from aioplate.gen_types import Imports
from aioplate.generator.imports_utils import update_imports
from aioplate.utils import camel_to_snake


class CodeWriter(Protocol):

    @abc.abstractmethod
    def middleware(self): ...

    @abc.abstractmethod
    def router(self): ...

    @abc.abstractmethod
    def project_level(self): ...


class StructureGenerator(Protocol):

    @abc.abstractmethod
    def generate_structure(self): ...


class ContentContext(Protocol):
    """Empty interface"""


# class FileContext:
#     def __init__(
#         self,
#         filename: str,
#         dir_path: Path,
#         code_contexts: list[ContentContext],
#     ):
#         self.filename = filename
#         self.code_contexts = code_contexts
#         self.dir_path = dir_path


# class ImportContext(ContentContext):
#     def __init__(self):
#         self.imports = collections.defaultdict(list)


@dataclass
class HandlerContext:
    name: str
    parameters: list[str]


@dataclass
class RouterContext(ContentContext):
    name: str
    imports: Imports
    handlers: list[HandlerContext]


@dataclass(frozen=True)
class MiddlewareContext(ContentContext):
    param_name: str
    class_name: str


@dataclass
class ConfigContext(ContentContext):
    configs: dict[str, dict[str, list[str]]] = field(default_factory=dict)


@dataclass
class ApplicationContext:
    config: ConfigContext
    src_layout: bool = True
    project_name: str = "generated"
    middlewares: dict[MiddlewareContext, set[int]] = field(
        default_factory=dict
    )  # middleware and needed registrations
    dispatcher_injections: set[str] = field(default_factory=set)
    # files: list[FileContext]
    routers: list[RouterContext] = field(default_factory=list)
    structure: Structure = IntroBotPlate()


class ApplicationBuilder:

    def __init__(self, app: ApplicationContext):
        self.app = app

    def dependency_applier(
        self,
        param_name: str | None,
        class_name: str,
        config: dict[str, list[str]] | None,
    ):
        if param_name:
            middle = MiddlewareContext(param_name, class_name)
            self.app.middlewares[middle] = set()
        else:
            injection = camel_to_snake(class_name)
            self.app.dispatcher_injections.add(injection)
        if config:
            self._add_config(class_name, config)

    def _add_config(self, class_: str, config: dict[str, list[str]]):
        self.app.config.configs[class_] = config

    def _add_dependency_usage(self, param: str, observer: int):
        for ctx in self.app.middlewares:
            if ctx.class_name == param:
                self.app.middlewares[ctx].add(observer)

    def _get_dependency_arg_name(self, dep: str):
        for ctx in self.app.middlewares:
            if ctx.class_name == dep:
                return ctx.param_name
        return camel_to_snake(dep)

    def add_handler_to_router(self, router_name: str, handler: HandlerContext, imports: Imports):
        for router in self.app.routers:
            if router.name == router_name:
                router.handlers.append(handler)
                update_imports(router.imports, imports)
                return
        router = RouterContext(router_name, imports, [handler])
        self.app.routers.append(router)

    def handler_applier(
        self,
        router,
        params: list[str],
        name: str,
    ):
        handler_args = []
        imports = {}
        if params[0] not in ("MESSAGE", "INLINE", "CALLBACK"):
            raise InvalidHandler
        for param in params:
            match param:
                case "MESSAGE":
                    handler_args.append("message: types.Message")
                case "INLINE":
                    handler_args.append("inline: types.InlineQuery")
                case "CALLBACK":
                    handler_args.append("call: types.CallbackQuery")
                case "STATE":
                    handler_args.append("state: FSMContext")
                    imports['aiogram.fsm.context'] = ['FSMContext']
                case "BOT":
                    handler_args.append("bot: Bot")
                    imports['aiogram'] = ['Bot']
                case "CALLBACK_DATA":
                    handler_args.append("callback_data: ...")
                    imports['aiogram.filters.callback_data'] = ['CallbackData']
                case _:
                    # elif type(param) is type and issubclass(param, Dependency):
                    if params[0] == "MESSAGE":
                        self._add_dependency_usage(param, MESSAGE)
                    elif params[0] == "INLINE":
                        self._add_dependency_usage(param, INLINE)
                    else:
                        self._add_dependency_usage(param, CALLBACK)
                    handler_args.append(f"{self._get_dependency_arg_name(param)}: ...")
        handler = HandlerContext(name, handler_args)
        self.add_handler_to_router(router, handler, imports)
