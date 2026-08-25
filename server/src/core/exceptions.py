"""
Custom Application Exceptions.
Follows rules/error-handling.md.
"""

class AppException(Exception):
    """Base application exception."""
    def __init__(self, message: str, error_code: str = "INTERNAL_SERVER_ERROR", status_code: int = 500, details: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}

class ValidationError(AppException):
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, error_code="VALIDATION_ERROR", status_code=400, details=details)

class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, error_code="NOT_FOUND", status_code=404)

class AuthenticationError(AppException):
    def __init__(self, message: str = "Authentication required or invalid token"):
        super().__init__(message, error_code="UNAUTHENTICATED", status_code=401)

class AuthorizationError(AppException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message, error_code="PERMISSION_DENIED", status_code=403)

class BatchLimitExceededError(AppException):
    def __init__(self, max_limit: int, actual_count: int):
        super().__init__(
            f"Jumlah batch proposal ({actual_count}) melebihi batas maksimum yang diizinkan ({max_limit})",
            error_code="BATCH_LIMIT_EXCEEDED",
            status_code=400,
            details={"max_limit": max_limit, "actual_count": actual_count}
        )

class DatabaseError(AppException):
    def __init__(self, message: str = "Terjadi kesalahan operasi database"):
        super().__init__(message, error_code="DATABASE_ERROR", status_code=500)

class ServiceUnavailableError(AppException):
    def __init__(self, message: str = "Layanan sedang warm-up atau belum siap"):
        super().__init__(message, error_code="SERVICE_UNAVAILABLE", status_code=503)
