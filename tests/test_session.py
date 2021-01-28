import pytest

from koji_builder_kube import session
from koji_builder_kube.session.session_ssl import SessionSSL
from koji_builder_kube import errors


def test_get_error():
  assert session.get('foorbar') is None


def test_get_success():
  s = session.get('ssl', serverca='ca.pem', cert='cert.pem')
  
  assert isinstance(s, SessionSSL)
