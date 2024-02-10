from dataclasses import dataclass

from aioplate.generator.imports_utils import ImportsRenderer
from aioplate.utils import camel_to_snake


@dataclass
class MiddlewareUsage:
    class_name: str
    inline: bool = False
    message: bool = False
    callback: bool = False


@dataclass
class MiddlewareGeneratorData(MiddlewareUsage):
    parameter_name: str = None


class MiddlewarePackageInitGenerator(ImportsRenderer):

    #  are keys - classes?
    #  todo code is possible to simplify (use key instead of _class_name)
    def __init__(
        self,
        middle_connects: dict[str, MiddlewareUsage],
        # main_module: MainModuleGenerator,
    ):
        # self.main_module = main_module
        self.middle_connects = middle_connects
        imports = {"aiogram": ["Dispatcher"]}
        for mc in middle_connects:
            imports["." + camel_to_snake(middle_connects[mc].class_name)] = [mc]
        self.imports = imports

    def _generate_init_middles(self) -> str:
        code = "\n\ndef init_middles(dp: Dispatcher):\n"
        middle_activation = "    dp.{}.outer_middleware({})\n"
        for mc in self.middle_connects:
            mc_val = self.middle_connects[mc]
            # if not (mc_val.inline or mc_val.callback or mc_val.message):
            #     continue
            snake_class_mw = camel_to_snake(mc_val.class_name) + "_mw"
            code += f"    {snake_class_mw} = {mc_val.class_name}()\n"
            if mc_val.message:
                code += middle_activation.format("message", snake_class_mw)
            if mc_val.callback:
                code += middle_activation.format("callback_query", snake_class_mw)
            if mc_val.inline:
                code += middle_activation.format("inline_query", snake_class_mw)
        return code

    def generate_init_middle_module(self) -> str:
        return self._get_imports() + self._generate_init_middles()


class MiddlewareGenerator(ImportsRenderer):
    def __init__(self, mgd: MiddlewareGeneratorData):
        self.mgd = mgd
        self.imports = {
            "typing": ["Any", "Callable", "Dict", "Union"],
            "aiogram": ["BaseMiddleware", "types"],
            "collections.abc": ["Awaitable"],
        }

    def _generate_middleware(self) -> str:
        event_types = []
        if self.mgd.message:
            event_types.append("types.Message")
        if self.mgd.callback:
            event_types.append("types.CallbackQuery")
        if self.mgd.inline:
            event_types.append("types.InlineQuery")
        if len(event_types) == 1:
            event_types = event_types[0]
        elif len(event_types) == 0:
            event_types = "..."
        else:
            event_types = f'Union[{", ".join(event_types)}]'
        code = f"""\n\nclass {self.mgd.class_name}(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[
            [{event_types}, Dict[str, Any]],
            Awaitable[Any],
        ],
        event: {event_types},
        data: Dict[str, Any],
    ):
        data["{self.mgd.parameter_name}"] = ...
        await handler(event, data)\n"""
        return code

    def generate_middleware_file_content(self) -> str:
        return self._get_imports() + self._generate_middleware()


@dataclass
class MiddlewarePackageGenerator:
    package_path: str
    middle_gen: list[MiddlewareGenerator]
    package_init: MiddlewarePackageInitGenerator
