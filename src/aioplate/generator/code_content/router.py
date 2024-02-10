from dataclasses import dataclass

from aioplate.gen_types import Imports
from aioplate.generator.imports_utils import ImportsRenderer, update_imports
from aioplate.utils import camel_to_snake


@dataclass
class HandlerData:
    name: str
    parameters: list[str]


class RouterGenerator(ImportsRenderer):
    def __init__(self, name: str, handlers: list[HandlerData], imports: Imports):
        self.name = camel_to_snake(name)
        self.handlers = handlers
        self.imports = {
            "aiogram": ["Router", "types"],
        }
        update_imports(self.imports, imports)

    def _generate_connected_handlers(self) -> str:
        code = f"""\n\n{self.name} = Router()\n"""
        state = False
        bot = False
        for handler in self.handlers:
            if not state and "state: FSMContext" in handler.parameters:
                state = True
                self.imports.update({"aiogram.fsm.context": ["FSMContext"]})
            if not bot and "bot: Bot" in handler.parameters:
                bot = True
                self.imports["aiogram"].append("Bot")
            code += "\n\n"
            if "message: types.Message" in handler.parameters:
                code += f"@{self.name}.message()\n"
            elif "call: types.CallbackQuery" in handler.parameters:
                code += f"@{self.name}.callback_query()\n"
            else:
                code += f"@{self.name}.inline_query()\n"
            code += (
                f'async def {handler.name}({", ".join(handler.parameters)}):\n    ...\n'
            )
        return code

    def generate_router(self) -> str:
        return self._get_imports() + self._generate_connected_handlers()


class RouterInitGenerator(ImportsRenderer):
    def __init__(self, router_imports: Imports):
        self.router_imports = router_imports
        self.imports = {"aiogram": ["Dispatcher"]}
        self.imports.update(router_imports)

    def _generate_router_init_function(self) -> str:
        routers = []
        for file in self.router_imports:
            for router in self.router_imports[file]:
                routers.append(router)
        code = "\n\ndef init_routers(dp: Dispatcher):\n"
        code += f'    dp.include_routers({", ".join(routers)},)\n'
        return code

    def generate_router_init(self) -> str:
        return self._get_imports() + self._generate_router_init_function()


@dataclass
class RouterPackageGenerator:
    package_path: str
    router_gens: list[RouterGenerator]
    package_init: RouterInitGenerator
