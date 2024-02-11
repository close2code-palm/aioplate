import warnings
from typing import cast

from aioplate.initial.entities import Folder
from aioplate.exceptions import NoRoutersPathToGenerate
from aioplate.initial.framework import CALLBACK, INLINE, MESSAGE, MIDDLEWARES, ROUTERS
from aioplate.generator.code_content.config import ConfigGenerator
from aioplate.generator.code_content.main import MainModuleGenerator
from aioplate.generator.code_content.middleware import (
    MiddlewareGenerator,
    MiddlewareGeneratorData,
    MiddlewarePackageGenerator,
    MiddlewarePackageInitGenerator,
)
from aioplate.generator.code_content.router import (
    HandlerData,
    RouterGenerator,
    RouterInitGenerator,
    RouterPackageGenerator,
)
from aioplate.extractor.constructor import (
    ApplicationContext,
    CodeWriter,
    StructureGenerator,
)
from aioplate.generator.structure import FSStructureGenerator
from aioplate.generator.writer import FSCodeWriter


def traverse_for_path(
    ctx: dict[str, str],
    dirs: list[Folder],
    prefix: str = "/",
):
    for f in dirs:
        module_path = prefix + f["name"]
        if "contains" in f:
            if f["contains"] == ROUTERS:
                ctx["routers"] = module_path
            elif f["contains"] == MIDDLEWARES:
                ctx["middlewares"] = module_path
        if "children" in f:
            traverse_for_path(ctx, f["children"], module_path + "/")


def get_modules_paths(project_layout: list[Folder]) -> tuple[str, str]:
    paths_ctx = {}
    traverse_for_path(paths_ctx, project_layout)
    return paths_ctx.get("middlewares"), paths_ctx.get("routers")


def get_import_path_from_path(path: str, app_ctx: ApplicationContext):
    parts = path.split("/")
    parts = filter(lambda s: s != "", parts)
    import_from = ".".join(parts)
    slug = "src." if app_ctx.src_layout else ""
    slug += f"{app_ctx.project_name}."
    return slug + import_from


def make_writer(ctx: ApplicationContext) -> CodeWriter:
    middle_in_main = bool(ctx.middlewares)
    middle_path, router_path = get_modules_paths(ctx.structure.project_layout)
    middle_imports_path = get_import_path_from_path(middle_path, ctx)
    router_imports_path = get_import_path_from_path(router_path, ctx)
    if not router_path:
        warnings.warn("no logics", NoRoutersPathToGenerate)
    middle_gen_datum = []
    for middle in ctx.middlewares:
        events = ctx.middlewares[middle]
        msg = MESSAGE in events
        call = CALLBACK in events
        inline = INLINE in events
        mgd = MiddlewareGeneratorData(
            parameter_name=middle.param_name,
            class_name=middle.class_name,
            message=msg,
            callback=call,
            inline=inline,
        )
        middle_gen_datum.append(mgd)

    router_generators = []
    router_imports: dict[str, list[str] | None] = {}
    for router in ctx.routers:
        handlers = cast(list[HandlerData], router.handlers)
        rg = RouterGenerator(router.name, handlers, router.imports)
        router_generators.append(rg)
        router_imports[f".{router.name}"] = [router.name]

    return FSCodeWriter(
        src=ctx.src_layout,
        project=ctx.project_name,
        config=ConfigGenerator(configs=ctx.config.configs),
        main=MainModuleGenerator(
            middle_in_main,
            injections=list(ctx.dispatcher_injections),
            imports={
                middle_imports_path: ["init_middles"],
                router_imports_path: ["init_routers"],
            },
        ),
        middles=MiddlewarePackageGenerator(
            middle_path,
            [MiddlewareGenerator(mgd) for mgd in middle_gen_datum],
            MiddlewarePackageInitGenerator(
                {mu.class_name: mu for mu in middle_gen_datum}
            ),
        ),
        routers=RouterPackageGenerator(
            router_path, router_generators, RouterInitGenerator(router_imports)
        ),
    )


def make_structure_initializer(app: ApplicationContext) -> StructureGenerator:
    return FSStructureGenerator(
        src=app.src_layout,
        project=app.project_name,
        structure=app.structure.project_layout,
    )
