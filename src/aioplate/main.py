from aioplate.generator.constructor import (
    ApplicationBuilder,
    ApplicationContext,
    ConfigContext,
)
from aioplate.generator.fs_factory import make_structure_initializer, make_writer
from aioplate.parser import parse_plate


def main():
    context = ApplicationContext(
        config=ConfigContext(),
    )
    code_builder = ApplicationBuilder(context)
    filename = "./plate.py"
    parse_plate(filename, builder=code_builder)
    writer = make_writer(code_builder.app)
    structure_builder = make_structure_initializer(code_builder.app)
    structure_builder.generate_structure()
    writer.project_level()
    writer.middleware()
    writer.router()


# if __name__ == "__main__":
#     main()
