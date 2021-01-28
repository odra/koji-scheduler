from typing import Optional, Any

from .session_ssl import SessionSSL
from .base import BaseSession


def get(name: str, **kwargs: Any) -> Optional[BaseSession]:
  for impl in [SessionSSL]:
    if impl.name() == name:
      return impl(**kwargs)
  return None
