class BaseError(Exception):
    pass


class FileError(BaseError):
    pass


class DirectoryError(BaseError):
    pass


class HTTPError(BaseError):
    pass
