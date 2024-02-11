from contextlib import suppress

from aioplate.gen_types import Imports


class ImportsRenderer:
    imports: Imports

    def _get_imports(self) -> str:
        import_part = []
        for import_source in self.imports:
            if (imps := self.imports[import_source]) is None:
                import_line = f"import {import_source}\n"
            elif not imps:
                continue
            else:
                imports = ", ".join(imps)
                import_line = f"from {import_source} import {imports}\n"
            import_part.append(import_line)

        return "".join(import_part)


def update_imports(target_imports: Imports, imports: Imports):
    for k in imports:
        try:
            if imports[k] and target_imports[k] is None:
                raise NotImplemented
        except KeyError:
            target_imports[k] = imports[k]
            continue
        for i in imports[k]:
            with suppress(KeyError):
                if i not in target_imports[k]:
                    target_imports[k].append(i)
