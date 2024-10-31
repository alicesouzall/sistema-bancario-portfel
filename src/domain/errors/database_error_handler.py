import psycopg
from domain.errors import UNKNOWN_ERROR

INVALID_UUID_ERROR = "the given uuid is invalid"
DATABASE_CONNECTION_FAILED_ERROR = "attempt to connect to the database failed"
DATABASE_CONNECTION_TIMEOUT_ERROR = "connection timeout"
DATABASE_PASSWORD_AUTHENTICATION_FAILED_ERROR = "password authentication failed"
DATABASE_PROGRAMMING_ERROR = "execution failed"
DATABASE_DATA_NOT_FOUND_ERROR = "data not found"
DATABASE_SYNTAX_ERROR = "syntax error"
DATABASE_COLUMN_NAME_NOT_FOUND_ERROR = "column name not found"
DATABASE_INVALID_COLUMN_NAME_ERROR = "invalid column name"
DATABASE_INVALID_DATA_TYPE_ERROR = "invalid data type"
DATABASE_TABLE_NOT_FOUND_ERROR = "table not found"
DATABASE_INVALID_PARAMETER_VALUE_ERROR = "invalid parameter value"
DATABASE_INVALID_PASSWORD_ERROR = "invalid password"
DATABASE_INTERNAL_ERROR = "internal error"
DATABASE_TOO_MANY_ARGUMENTS_ERROR = "too many arguments"
DATABASE_FOREIGN_KEY_VIOLATION_ERROR = "foreign key violation"
DATABASE_ATTRIBUTE_ERROR = "attribute error"
DATABASE_UNDEFINED_TABLE_ERROR = "undefined table"
DATABASE_UNDEFINED_COLUMN_ERROR = "undefined column"
DATABASE_OPERATIONAL_ERROR = "operational_error"
USER_ALREADY_EXISTS_ERROR = "user already exists"

class DatabaseErrorHandler:
    def handle_pg_connection_exceptions(self, error: Exception):
        match error.__class__:
            case psycopg.OperationalError:
                raise DatabaseOperationalError(custom_args=error.args[0])
            case psycopg.errors.InvalidPassword:
                raise InvalidPassword(custom_args=error.args[0])
            case psycopg.errors.ConnectionTimeout:
                raise DatabaseConnectionError(
                    custom_args=DATABASE_CONNECTION_TIMEOUT_ERROR
                )
            case _:
                raise error

    def handle_pg_exceptions(self, error: Exception):
        match error.__class__:
            case psycopg.ProgrammingError:
                raise ProgrammingError(custom_args=error.args[0])
            case psycopg.errors.NoDataFound:
                raise DataNotFound(custom_args=error.args[0])
            case psycopg.errors.SyntaxError:
                raise SyntaxError(custom_args=error.args[0])
            case psycopg.errors.FdwColumnNameNotFound:
                raise ColumnNameNotFound(custom_args=error.args[0])
            case psycopg.errors.FdwInvalidColumnName:
                raise InvalidColumnName(custom_args=error.args[0])
            case psycopg.errors.FdwInvalidDataType:
                raise InvalidDataType(custom_args=error.args[0])
            case psycopg.errors.FdwTableNotFound:
                raise TableNotFound(custom_args=error.args[0])
            case psycopg.errors.InvalidParameterValue:
                raise InvalidParameterValue(custom_args=error.args[0])
            case psycopg.errors.InternalError:
                raise InternalError(custom_args=error.args[0])
            case psycopg.errors.TooManyArguments:
                raise TooManyArguments(custom_args=error.args[0])
            case psycopg.errors.ForeignKeyViolation:
                raise ForeignKeyViolation(custom_args=error.args[0])
            case psycopg.errors.UndefinedTable:
                raise UndefinedTable(custom_args=error.args[0])
            case psycopg.errors.UndefinedColumn:
                raise UndefinedColumn(custom_args=error.args[0])
            case _:
                raise UnknownError(custom_args=error.args)

class ProgrammingError(Exception):
    def __init__(self, custom_args = None, message = DATABASE_PROGRAMMING_ERROR, code = 500):
        self.message = message
        self.log_message = f"{message} -> {custom_args}"
        self.code = code
        super().__init__(self.message, self.message, self.code)

class DataNotFound(Exception):
    def __init__(self, custom_args = None, message = DATABASE_DATA_NOT_FOUND_ERROR, code = 500):
        self.message = message
        self.log_message = f"{message} -> {custom_args}"
        self.code = code
        super().__init__(self.message, self.message, self.code)

class SyntaxError(Exception):
    def __init__(self, custom_args = None, message = DATABASE_SYNTAX_ERROR, code = 500):
        self.message = message
        self.log_message = f"{message} -> {custom_args}"
        self.code = code
        super().__init__(self.message, self.message, self.code)

class ColumnNameNotFound(Exception):
    def __init__(self, custom_args = None, message = DATABASE_COLUMN_NAME_NOT_FOUND_ERROR, code = 500):
        self.message = message
        self.log_message = f"{message} -> {custom_args}"
        self.code = code
        super().__init__(self.message, self.message, self.code)

class InvalidColumnName(Exception):
    def __init__(self, custom_args = None, message = DATABASE_INVALID_COLUMN_NAME_ERROR, code = 500):
        self.message = message
        self.log_message = f"{message} -> {custom_args}"
        self.code = code
        super().__init__(self.message, self.message, self.code)

class InvalidDataType(Exception):
    def __init__(self, custom_args = None, message = DATABASE_INVALID_DATA_TYPE_ERROR, code = 500):
        self.message = message
        self.log_message = f"{message} -> {custom_args}"
        self.code = code
        super().__init__(self.message, self.message, self.code)

class TableNotFound(Exception):
    def __init__(self, custom_args = None, message = DATABASE_TABLE_NOT_FOUND_ERROR, code = 500):
        self.message = message
        self.log_message = f"{message} -> {custom_args}"
        self.code = code
        super().__init__(self.message, self.message, self.code)

class InvalidParameterValue(Exception):
    def __init__(self, custom_args = None, message = DATABASE_INVALID_PARAMETER_VALUE_ERROR, code = 500):
        self.message = message
        self.log_message = f"{message} -> {custom_args}"
        self.code = code
        super().__init__(self.message, self.message, self.code)

class InvalidPassword(Exception):
    def __init__(self, custom_args = None, message = DATABASE_INVALID_PASSWORD_ERROR, code = 500):
        self.message = message
        self.log_message = f"{message} -> {custom_args}"
        self.code = code
        super().__init__(self.message, self.message, self.code)

class InternalError(Exception):
    def __init__(self, custom_args = None, message = DATABASE_INTERNAL_ERROR, code = 500):
        self.message = message
        self.log_message = f"{message} -> {custom_args}"
        self.code = code
        super().__init__(self.message, self.message, self.code)

class TooManyArguments(Exception):
    def __init__(self, custom_args = None, message = DATABASE_TOO_MANY_ARGUMENTS_ERROR, code = 500):
        self.message = message
        self.log_message = f"{message} -> {custom_args}"
        self.code = code
        super().__init__(self.message, self.message, self.code)

class ForeignKeyViolation(Exception):
    def __init__(self, custom_args = None, message = DATABASE_FOREIGN_KEY_VIOLATION_ERROR, code = 500):
        self.message = message
        self.log_message = f"{message} -> {custom_args}"
        self.code = code
        super().__init__(self.message, self.message, self.code)

class UndefinedTable(Exception):
    def __init__(self, custom_args = None, message = DATABASE_UNDEFINED_TABLE_ERROR, code = 500):
        self.message = message
        self.log_message = f"{message} -> {custom_args}"
        self.code = code
        super().__init__(self.message, self.message, self.code)

class UndefinedColumn(Exception):
    def __init__(self, custom_args = None, message = DATABASE_UNDEFINED_COLUMN_ERROR, code = 500):
        self.message = message
        self.log_message = f"{message} -> {custom_args}"
        self.code = code
        super().__init__(self.message, self.message, self.code)

class DatabaseAttributeError(Exception):
    def __init__(self, custom_args = None, message = DATABASE_ATTRIBUTE_ERROR, code = 500):
        self.message = message
        self.log_message = f"{message} -> {custom_args}"
        self.code = code
        super().__init__(self.message, self.message, self.code)

class UnknownError(Exception):
    def __init__(self, custom_args = None, message = UNKNOWN_ERROR, code = 500):
        self.message = message
        self.log_message = f"{message} -> {custom_args}"
        self.code = code
        super().__init__(self.message, self.message, self.code)

class DatabaseConnectionError(Exception):
    def __init__(self, custom_args = None, message = DATABASE_CONNECTION_FAILED_ERROR, code = 500):
        self.message = message
        self.log_message = f"{message} -> {custom_args}"
        self.code = code
        super().__init__(self.message, self.message, self.code)

class DatabaseOperationalError(Exception):
    def __init__(self, custom_args = None, message = DATABASE_OPERATIONAL_ERROR, code = 500):
        self.message = message
        self.log_message = f"{message} -> {custom_args}"
        self.code = code
        super().__init__(self.message, self.message, self.code)
