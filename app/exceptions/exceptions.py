

class ApplicationError(Exception):
    """Базовое исключение приложения"""
    pass

class Forbidden(ApplicationError):
    """Недостаточно прав"""
    pass

class NotFound(ApplicationError):
    """Объект не найден"""
    pass

class BusinessError(ApplicationError):
    """Объект не найден"""
    pass