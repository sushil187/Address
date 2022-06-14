class BaseException(Exception):
    ...


class NotFoundError(BaseException):
    def __init__(self, msg: str):
        self.status_code = 404
        self.detail = msg


class AlreadyExistError(BaseException):
    def __init__(self, msg: str):
        self.status_code = 409
        self.detail = msg
