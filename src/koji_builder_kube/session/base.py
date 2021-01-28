from typing import Any, Callable
from typing_extensions import Protocol


class BaseSession(Protocol):
  """
  Base Session protocol class to be inherited by
  specialized implementation classes.
  """

  @staticmethod
  def name() -> str:
    """
    Return the unique name of the session implementation.

    This is a static method.
    """
    pass

  def preflight_check(self) -> None:
    """
    Checks to run before authentication, such as if certificate path is valid.

    Should raise `errors.KojiError` to indicate failure. 
    """
    pass

  def login(self) -> None:
    """
    Authenticates to a koji-hub instance.
    Raises an AuthError in case of failure.
    """
    pass

  def is_ok(self) -> bool:
    """
    Return a boolean value validating the session status.
    """
    pass

  def logout(self) -> None:
    """
    Destroys the current session.
    Raises an AuthError in case of failure.
    """
    pass
