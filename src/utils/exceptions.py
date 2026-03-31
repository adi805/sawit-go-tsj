"""
Sawit Go - TSJ - Custom Exceptions
"""


class SawitGoException(Exception):
    """Base exception for Sawit Go"""
    
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code or "ERR_UNKNOWN"
        super().__init__(self.message)


class ValidationError(SawitGoException):
    """Validation errors"""
    
    def __init__(self, message: str, field: str = None):
        super().__init__(message, "ERR_VALIDATION")
        self.field = field


class DatabaseError(SawitGoException):
    """Database errors"""
    
    def __init__(self, message: str, original_error: Exception = None):
        super().__init__(message, "ERR_DATABASE")
        self.original_error = original_error


class AuthenticationError(SawitGoException):
    """Authentication errors"""
    
    def __init__(self, message: str):
        super().__init__(message, "ERR_AUTH")


class AuthorizationError(SawitGoException):
    """Authorization errors"""
    
    def __init__(self, message: str):
        super().__init__(message, "ERR_AUTHORIZATION")


class BusinessRuleError(SawitGoException):
    """Business rule violations"""
    
    def __init__(self, message: str, rule_id: str = None):
        super().__init__(message, "ERR_BUSINESS_RULE")
        self.rule_id = rule_id


class JournalValidationError(ValidationError):
    """Journal entry validation errors"""
    
    def __init__(self, message: str, line_number: int = None):
        super().__init__(message)
        self.code = "ERR_JOURNAL_VALIDATION"
        self.line_number = line_number


class AccountError(SawitGoException):
    """Account-related errors"""
    
    def __init__(self, message: str, account_code: str = None):
        super().__init__(message, "ERR_ACCOUNT")
        self.account_code = account_code
