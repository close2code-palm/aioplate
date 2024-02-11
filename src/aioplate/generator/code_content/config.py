from aioplate.generator.imports_utils import ImportsRenderer
from aioplate.utils import camel_to_snake


class ConfigGenerator(ImportsRenderer):
    def __init__(self, configs: dict[str, dict[str, list[str]]]):
        self.imports = {
            "pydantic": ["BaseModel"],
            "os": None,
            "contextlib": ["suppress"],
            "typing": ["TextIO"],
        }
        self.configs = {"Telegram": {"str": ["TOKEN"]}}
        self.configs.update(configs)

    def generate_configs(self) -> str:
        imports = self._get_imports()
        classes = self._generate_config_classes()
        functions = self._generate_functions()
        return imports + classes + functions

    def generate_template(self) -> str:
        env_content = ""
        for c in self.configs:
            for k in self.configs[c]:
                for field in self.configs[c][k]:
                    env_content += f"{field}=\n"
        return env_content

    def _generate_config_classes(self) -> str:
        general_fields = {}
        classes = ""
        for config in self.configs:
            code = f"\n\nclass {config}(BaseModel):\n"
            general_fields[config] = camel_to_snake(config)
            for k in self.configs[config]:
                for field in self.configs[config][k]:
                    code += f"    {field.lower()}: {k}\n"
            classes += code
        config_code = "\n\nclass Config(BaseModel):\n"
        for k in general_fields:
            config_code += f"    {general_fields[k]}: {k}\n"
        return classes + config_code

    def _generate_functions(self):
        functions = ""
        parse_env_source = """\n\ndef parse_to_env(env_file: TextIO):
    for line in env_file.readlines():
        if "=" in line:
            k, v = line.split("=")
            os.environ[k] = v.strip()\n"""
        functions += parse_env_source
        read_config_source = """\n\ndef read_config(env_path: str | None = None) -> Config:
    if env_path:
        with suppress(FileNotFoundError):
            with open(env_path) as env_file:
                parse_to_env(env_file)\n"""
        functions += read_config_source
        models_init = ""
        config_init = ""
        for config in self.configs:
            snake_config = camel_to_snake(config)
            code = f"    {snake_config} = {config}(\n"
            config_init += f"        {snake_config}={snake_config},\n"
            for k in self.configs[config]:
                for field in self.configs[config][k]:
                    env_var = f"os.environ.get('{field}')"
                    valid_env = f"{k}({env_var})" if k != "str" else env_var
                    code += f"        {field.lower()}={valid_env},\n"
            code += "    )\n"
            models_init += code
        result_model_ret = "    return Config(\n" + config_init + "    )\n"

        return functions + models_init + result_model_ret
