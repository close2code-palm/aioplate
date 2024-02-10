import re


def camel_to_snake(camel_name: str):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", camel_name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
