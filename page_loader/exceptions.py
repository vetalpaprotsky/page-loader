import requests


class NetworkError(requests.exceptions.RequestException):
    pass


class StorageError(OSError):
    pass
