def make_init_file():
    with open("plate.py", "w") as f:
        f.write(
            """\"\"\"Commented lines will not be included in init command, but will in example\"\"\"

from aioplate.initial.framework import (
    MESSAGE,
    CALLBACK,
    INLINE,
    CALLBACK_DATA,
    BOT,
    STATE,
)
from aioplate.initial.entities import (
    Dependency,
    Router,
    Handler,
)


PROJECT_NAME = "it_works"

# PROJECT_NAME - name of the root package


# Dependencies are injected directly through dispatcher if no parameter,
# middleware generated otherwise
# configs are dicts: type - variables of that type in list (TOKEN is predefined)
# dependency name is inferred from class name, as well as router and handlers names

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
    

class GithubApiHTTPConnector(Dependency):
    # config = {'str': ['GITHUB_TOKEN']}
    ...


class IntroRouter(Router):
    pass
    # filename = "intro"
    # parent = Dispatcher


class BotRouter(Router):
    pass


# MESSAGE, INLINE or CALLBACK should be first in tuple `parameters`


class StartHandler(Handler):
    parameters = MESSAGE,  # tuples only!
    router = IntroRouter  # maybe by position?


class SaveMe(Handler):
    parameters = MESSAGE, SQLAlchemyRepo
    router = IntroRouter


class DumbState(Handler):
    parameters = CALLBACK, STATE
    router = IntroRouter


class DumbBot(Handler):
    parameters = INLINE, SQLAlchemyRepo, BOT
    router = BotRouter

"""
        )


# if __name__ == '__main__':
#     main()
