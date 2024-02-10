class AioPlateException(Exception):

    def __str__(self):
        return """Base application error."""


class InvalidHandler(AioPlateException):

    def __str__(self):
        return """First argument should be telegram event."""


class NoRoutersPathToGenerate(Warning):

    def __str__(self):
        return """No router path specified."""
