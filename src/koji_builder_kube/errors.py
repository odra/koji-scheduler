import errno

from typing import Dict, Any, Optional


class BaseError(Exception):
  """
  Base error class.
  """
  code: int
  message: str
  data: Optional[Dict[str, Any]]

  def __init__(self, message: str, code: int, data: Optional[Dict[str, Any]] = None):
    super(BaseError, self).__init__(message)
    self.code = code
    self.message = message
    self.data = data

  def __repr__(self) -> str:
    return f'[{self.code}] {self.message}'


class KojiError(BaseError):
  """
  Specialized error class for generic error across the project.
  """
  def __init__(self, message: str = 'unexpected koji error', data: Optional[Dict[str, Any]] = None):
    super(KojiError, self).__init__(message, 1, data)


class AuthError(BaseError):
  """
  Specialized error class for authentication errors.
  """
  def __init__(self, message: Optional[str] = None, data: Optional[Dict[str, Any]] = None):
    super(AuthError, self).__init__(f'AuthError: {message}', errno.EACCES, data)
