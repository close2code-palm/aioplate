from aioplate.generator.code_content.config import ConfigGenerator
from aioplate.generator.code_content.main import MainModuleGenerator
from aioplate.generator.code_content.middleware import MiddlewarePackageGenerator
from aioplate.generator.code_content.router import RouterPackageGenerator
from aioplate.extractor.constructor import CodeWriter
from aioplate.utils import camel_to_snake


def write_code(filename: str, path: str, code: str, ext: str = "py"):
    with open(f"{path}/{filename}.{ext}", "w+") as f:
        f.write(code)


class FSCodeWriter(CodeWriter):
    def __init__(
        self,
        src: bool,
        project: str,
        config: ConfigGenerator,
        main: MainModuleGenerator,
        middles: MiddlewarePackageGenerator | None,
        routers: RouterPackageGenerator,
    ):
        self.main = main
        self.config = config
        self.middles = middles
        self.routers = routers
        self.prefix = f"/{project}"
        if src:
            self.prefix = "/src" + self.prefix
        self.prefix = "." + self.prefix

    def project_level(self):
        code_main = self.main.generate_main()
        write_code("main", self.prefix, code_main)
        code_config = self.config.generate_configs()
        write_code("config", self.prefix, code_config)
        env_template = self.config.generate_template()
        write_code("", ".", env_template, "env")

    def middleware(self):
        folder = f"{self.prefix}/{self.middles.package_path}"
        for mg in self.middles.middle_gen:
            code = mg.generate_middleware_file_content()
            filename = camel_to_snake(mg.mgd.class_name)
            write_code(filename, folder, code)
        init_code = self.middles.package_init.generate_init_middle_module()
        write_code("__init__", folder, init_code)

    def router(self):
        folder = f"{self.prefix}/{self.routers.package_path}"
        for router in self.routers.router_gens:
            code = router.generate_router()
            write_code(router.name, folder, code)
        init_code = self.routers.package_init.generate_router_init()
        write_code("__init__", folder, init_code)
