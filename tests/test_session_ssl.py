import pytest

from koji_builder_kube.session.session_ssl import SessionSSL
from koji_builder_kube import errors


def test_name():
  assert SessionSSL.name() == 'ssl'


def test_preflight_check_error():
  s = SessionSSL('ca', 'cert', 'key')
  with pytest.raises(errors.KojiError):
    s.preflight_check()


def test_preflight_check_success(fixtures_dir):
  s = SessionSSL(f'{fixtures_dir}/ca.pem',
    f'{fixtures_dir}/cert.pem',
    f'{fixtures_dir}/key.pem')
  s.preflight_check()


def test_is_ok_error_session_null():
  s = SessionSSL('ca', 'cert', 'key')
  with pytest.raises(errors.KojiError) as e:
    s.is_ok()
  
  expected = '[1] Session was not initialized'
  current = repr(e.value)
  
  assert expected ==  current
