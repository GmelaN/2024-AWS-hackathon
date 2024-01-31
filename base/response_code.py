from enum import Enum

class ResponseCode(Enum):
    SUCCESS = "SUCCESS", 200
    NOT_FOUND = "NOT_FOUND", 404
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR", 500
    BAD_REQUEST = "BAD_REQUEST", 400

    def __init__(self, message, http_status):
        self.message = message
        self.http_status = http_status
