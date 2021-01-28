import os
import configparser

from typing import Dict, Any

from koji_builder_kube import errors


class Config:
  config: configparser.ConfigParser

  @classmethod
  def from_path(cls, path: str) -> 'Config':
    if not os.path.exists(path):
      raise errors.KojiError(f'Config file not found: {path}')
    config = configparser.ConfigParser()
    try:
      config.read(path)
    except configparser.Error as e:
      raise errors.KojiError(str(e))
    c = cls()
    c.config = config
    return c

  def section(self, name: str) -> Dict[str, str]:
    try:
      return {k:v for k,v in self.config.items(name)}
    except configparser.Error as e:
      return {}