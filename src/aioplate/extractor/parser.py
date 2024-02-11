import ast

from aioplate.extractor.constructor import ApplicationBuilder
from aioplate.utils import camel_to_snake


def parse_plate(path: str, builder: ApplicationBuilder):
    with open(path) as f:
        plate_ast = ast.parse(f.read())
    for stmt in plate_ast.body:
        if type(stmt) is ast.Assign:
            if stmt.targets[0].id == "PROJECT_NAME":
                builder.app.project_name = stmt.value.value
        elif type(stmt) is ast.ClassDef:
            if not len(stmt.bases) == 1:
                raise SyntaxError(
                    "Each class should be inherited exactly once",
                    (path, stmt.lineno, stmt.end_col_offset, stmt.name),
                )
            first_base = stmt.bases[0]
            match first_base.id:
                case "Dependency":
                    dep_map = {}
                    for body_stmt in stmt.body:
                        if type(body_stmt) is ast.Assign:
                            if body_stmt.targets[0].id == "parameter_name":
                                dep_map["parameter_name"] = body_stmt.value.value
                            elif body_stmt.targets[0].id == "config":
                                dep_map["config"] = {}
                                for i, k in enumerate(body_stmt.value.keys):
                                    dep_map["config"][k.value] = [
                                        e.value for e in body_stmt.value.values[i].elts
                                    ]
                    builder.dependency_applier(
                        dep_map.get("parameter_name"), stmt.name, dep_map.get("config")
                    )
                # case "Router":
                #     _ = stmt.name
                case "Handler":
                    handler = {"parameters": []}
                    for body_stmt in stmt.body:
                        if type(body_stmt) is ast.Assign:
                            if body_stmt.targets[0].id == "router":
                                handler["router"] = body_stmt.value.id
                            elif body_stmt.targets[0].id == "parameters":
                                for param in body_stmt.value.elts:
                                    handler["parameters"].append(param.id)
                    builder.handler_applier(
                        camel_to_snake(handler["router"]),
                        handler["parameters"],
                        camel_to_snake(stmt.name),
                    )
