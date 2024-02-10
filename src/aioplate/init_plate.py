def make_init_file():
    with open("plate.py", "w") as f:
        f.write(
            """\"\"\"Commented lines will not be included in init command, but will in example\"\"\"

from aioplate.framework import (
    MESSAGE,
    CALLBACK,
    INLINE,
    BOT,
    CALLBACK_DATA,
    Dispatcher,
    STATE,
)  # todo replace this with aiogram`s std
from aioplate.entities import (
    Dependency,
    Router,
    Structure,
    FolderKeys,
    Handler,
    Setup,
)


PROJECT_NAME = "generated"


class SQLAlchemyRepo(Dependency):
    parameter_name = "repo"  # if used - treats dep as middleware
    config = {
        "str": [
            "DB",
            "USER",
            "PASSWORD",
            "HOST",
        ],
        "int": ["PORT"],
    }


class GithubApiHTTPConnector(Dependency): ...


class IntroRouter(Router):
    filename = "intro"
    # parent = Dispatcher


class StartHandler(Handler):
    parameters = (MESSAGE,)
    router = IntroRouter  # maybe by position?


class SaveMe(Handler):
    parameters = MESSAGE, SQLAlchemyRepo
    router = IntroRouter
"""
        )


# if __name__ == '__main__':
#     main()
