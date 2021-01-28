from koji_builder_kube import errors


def test_error_default():
  e = errors.AuthError()

  assert e.message == 'AuthError: None'
  assert e.code == 13
  assert e.data is None
  assert repr(e) == '[13] AuthError: None'


def test_error_custom():
  e = errors.AuthError('SSL AUTH', data={'cert': '/tmp/cert.pem'})

  assert e.message == 'AuthError: SSL AUTH'
  assert e.code == 13
  assert e.data == {'cert': '/tmp/cert.pem'}
  assert repr(e) == '[13] AuthError: SSL AUTH'
