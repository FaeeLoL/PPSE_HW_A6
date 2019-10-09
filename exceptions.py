class InvalidTypeException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args)


class InvalidExpressionException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args)


class InvalidHistoryCallException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args)


class YaDaunException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args)


class IncompatibleException(TypeError):
    def __init__(self, *args, **kwargs):
        TypeError.__init__(self, *args, **kwargs)
