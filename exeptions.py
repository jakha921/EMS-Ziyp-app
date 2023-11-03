from fastapi import HTTPException, status


class BookingException(HTTPException):  # <-- наследуемся от HTTPException, который наследован от Exception
    status_code = 500  # <-- задаем значения по умолчанию
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsWithThisEmailException(BookingException):  # # <-- наследуемся от BookingException
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists with this email"


class UserNotFoundException(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"


class NotAuthenticatedException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Not authenticated"

