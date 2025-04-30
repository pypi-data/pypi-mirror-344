import json
from flask import Response


class NestpyException(Exception):
    def __init__(self, message: str = "Internal Server Error", status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class BadRequestException(NestpyException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(message, 400)


class UnauthorizedException(NestpyException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401)


class NotFoundException(NestpyException):
    def __init__(self, message: str = "Not found"):
        super().__init__(message, 404)


class ForbiddenException(NestpyException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, 403)


class NotAcceptableException(NestpyException):
    def __init__(self, message: str = "Not Acceptable"):
        super().__init__(message, 406)


class RequestTimeoutException(NestpyException):
    def __init__(self, message: str = "Request Timeout"):
        super().__init__(message, 408)


class ConflictException(NestpyException):
    def __init__(self, message: str = "Conflict"):
        super().__init__(message, 409)


class GoneException(NestpyException):
    def __init__(self, message: str = "Gone"):
        super().__init__(message, 410)


class HttpVersionNotSupportedException(NestpyException):
    def __init__(self, message: str = "HTTP version not supported"):
        super().__init__(message, 505)


class PayloadTooLargeException(NestpyException):
    def __init__(self, message: str = "Payload too large"):
        super().__init__(message, 413)


class UnsupportedMediaTypeException(NestpyException):
    def __init__(self, message: str = "Unsupported media type"):
        super().__init__(message, 415)


class UnprocessableEntityException(NestpyException):
    def __init__(self, message: str = "Unprocessable entity"):
        super().__init__(message, 422)


class InternalServerErrorException(NestpyException):
    def __init__(self, message: str = "Internal server error"):
        super().__init__(message, 500)


class NotImplementedException(NestpyException):
    def __init__(self, message: str = "Not implemented"):
        super().__init__(message, 501)


class ImATeapotException(NestpyException):
    def __init__(self, message: str = "I'm a teapot"):
        super().__init__(message, 418)


class MethodNotAllowedException(NestpyException):
    def __init__(self, message: str = "Method not allowed"):
        super().__init__(message, 405)


class BadGatewayException(NestpyException):
    def __init__(self, message: str = "Bad gateway"):
        super().__init__(message, 502)


class ServiceUnavailableException(NestpyException):
    def __init__(self, message: str = "Service unavailable"):
        super().__init__(message, 503)


class GatewayTimeoutException(NestpyException):
    def __init__(self, message: str = "Gateway timeout"):
        super().__init__(message, 504)


class PreconditionFailedException(NestpyException):
    def __init__(self, message: str = "Precondition failed"):
        super().__init__(message, 412)


def nestpy_exception_handler(e: NestpyException):
    """Return JSON instead of HTML for HTTP errors."""
    return Response(
        response=json.dumps(
            {
                "message": str(e),
                "statusCode": e.status_code,
            }
        ),
        status=e.status_code,
        content_type="application/json",
    )
