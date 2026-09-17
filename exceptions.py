class PharmacyException(Exception):
    """Base exception for pharmacy management system"""
    pass

class ValidationError(PharmacyException):
    """Raised when input validation fails"""
    pass

class NotFoundException(PharmacyException):
    """Raised when a requested resource is not found"""
    pass

class DatabaseError(PharmacyException):
    """Raised when a database operation fails"""
    pass

class AuthenticationError(PharmacyException):
    """Raised when authentication fails"""
    pass

class AuthorizationError(PharmacyException):
    """Raised when user doesn't have required permissions"""
    pass 