from enum import Enum


class AuthActions(str, Enum):
    REGISTER = 'register'
    LOGIN = 'login'
    LOGOUT = 'logout'
    ME = 'me'
