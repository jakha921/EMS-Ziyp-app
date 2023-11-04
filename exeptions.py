from fastapi import HTTPException, status


class BookingException(HTTPException):  # <-- наследуемся от HTTPException, который наследован от Exception
    status_code = 500  # <-- задаем значения по умолчанию
    detail = ""

    def __init__(self, detail: str = None):
        if detail is not None:
            self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsWithThisEmailException(BookingException):  # # <-- наследуемся от BookingException
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists with this email"


class UserNotFoundException(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"

    def __init__(self, detail: str = None):
        super().__init__(detail=detail)


class NotFoundException(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Module not found"

    def __init__(self, detail: str = None):
        super().__init__(detail=detail)


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"


class NotAuthenticatedException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Not authenticated"


class NotAuthorizedException(BookingException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Not authorized"


class NotValidCredentialsException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Could not validate credentials"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"


class VolunteerAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Volunteer already exists"


# get detail from exception object
class AlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Already exists"

    def __init__(self, detail: str = None):
        super().__init__(detail=detail)
