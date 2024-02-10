from aioplate.gen_types import Imports
from aioplate.generator.imports_utils import ImportsRenderer


class MainModuleGenerator(ImportsRenderer):

    def __init__(self, middles: bool, injections: list[str], imports: Imports):
        self.imports = {
            "config": ["read_config"],
            "aiogram": ["Bot", "Dispatcher"],
        }
        self.imports.update(imports)
        self.injections = injections
        self.middles = middles

    def generate_main(self):
        return self._get_imports() + self._generate_main()

    def _apply_injections(self) -> str:
        injections = ""
        for i in self.injections:
            injections += f"    {i} = ...\n"
            injections += f'    dp["{i}"] = {i}\n'
        return injections

    def _generate_main(self) -> str:
        main = (
            "\n\ndef main():\n"
            '    config = read_config(".env")\n'
            "    bot = Bot(token=...)\n"
            "    dp = Dispatcher()\n"
            "    init_routers(dp)\n"
        )
        main += self._apply_injections()
        if self.middles:
            main += "    init_middles(dp, config)\n"
        main += "    dp.run_polling(bot)\n\n\n"
        main += 'if __name__ == "__main__":\n'
        main += "    main()\n"
        return main
