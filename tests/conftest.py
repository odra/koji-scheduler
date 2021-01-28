import os

import pytest


@pytest.fixture
def cwd():
  return os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def fixtures_dir(cwd):
  return f'{cwd}/fixtures'
