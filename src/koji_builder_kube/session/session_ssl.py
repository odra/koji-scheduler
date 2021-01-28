import os

from typing import Any, Optional, Dict

from .base import BaseSession
from koji_builder_kube import errors
import types
import requests

import koji # type: ignore


class SessionSSL(BaseSession):
  """
  Base Session protocol class to be inherited by
  specialized implementation classes.
  """
  opts: Dict[Any, Any]
  session: Optional[Any] = None
  
  @staticmethod
  def name() -> str:
    return 'ssl'

  def __init__(self, **kwargs: Any) -> None:
    self.opts = kwargs

  def preflight_check(self) -> None:
    paths = [self.opts['cert'], self.opts['serverca']]
    for path in paths:
      if not os.path.exists(path):
        raise errors.KojiError(f'File not found: {path}')

  def login(self) -> None:
    """
    Authenticates to a koji-hub instance.
    Raises an AuthError in case of failure.
    """
    self.session = koji.ClientSession(self.opts['server'], self.opts)
    try:
      self.session.ssl_login(self.opts['cert'], None, self.opts['serverca'])
    except requests.exceptions.RequestException as e:
      raise errors.KojiError(str(e))
    except koji.AuthError as e:
      raise errors.AuthError(str(e),
        data={'ca_cert': self.opts['serverca'], 'cert': self.opts['cert']})

  def is_ok(self) -> bool:
    """
    Return a boolean value validating the session status.
    """
    if self.session is None:
      raise errors.KojiError('Session was not initialized')
    return True

  def logout(self) -> None:
    """
    Destroys the current session.
    Raises an AuthError in case of failure.
    """
    if self.session is None:
      raise errors.KojiError('Session was not initialized or is already terminated')
    try:
      self.session.logout()
    except koji.AuthError as e:
      raise errors.AuthError(str(e),
        data={'ca_cert': self.opts['serverca'], 'cert': self.opts['cert']})
    self.session = None
