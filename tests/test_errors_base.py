from koji_builder_kube import errors


def test_error_default():
  e = errors.BaseError('foo', 1)

  assert e.message == 'foo'
  assert e.code == 1
  assert e.data is None
  assert repr(e) == '[1] foo'


def test_error_custom():
  e = errors.BaseError('file exists', 17, data={'path': '/home'})

  assert e.message == 'file exists'
  assert e.code == 17
  assert e.data == {'path': '/home'}
  assert repr(e) == '[17] file exists'
