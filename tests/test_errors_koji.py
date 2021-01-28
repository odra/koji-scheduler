from koji_builder_kube import errors


def test_error_default():
  e = errors.KojiError()

  assert e.message == 'unexpected koji error'
  assert e.code == 1
  assert e.data is None
  assert repr(e) == '[1] unexpected koji error'


def test_error_custom():
  e = errors.KojiError('host is down', data={'url': 'localhost:8443'})

  assert e.message == 'host is down'
  assert e.code == 1
  assert e.data == {'url': 'localhost:8443'}
  assert repr(e) == '[1] host is down'
