"""
Custom exceptions used by Tech Loan api.
"""


class MissingParamException(Exception):
    pass


class InvalidParamException(Exception):
    pass


class NotFoundException(Exception):
    pass
