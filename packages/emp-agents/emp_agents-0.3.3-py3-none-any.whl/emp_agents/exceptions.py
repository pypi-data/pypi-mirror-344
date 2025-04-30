class TooManyTriesException(BaseException):
    pass


class InvalidModelException(BaseException):
    pass


class DuplicateToolException(BaseException):
    """This happens if two tools with the same name are added"""
