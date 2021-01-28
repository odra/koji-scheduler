import pytest

from koji_builder_kube.config import Config
from koji_builder_kube import errors


def test_from_path_error_path():
  with pytest.raises(errors.KojiError):
    Config.from_path('/something')


def test_from_path_error_format(fixtures_dir):
  with pytest.raises(errors.KojiError) as e:
    Config.from_path(f'{fixtures_dir}/kojid-invalid.conf')

  assert 'File contains no section headers.' in str(e.value)


def test_from_path_success(fixtures_dir):
  c = Config.from_path(f'{fixtures_dir}/kojid-ssl.conf')
  
  assert ['kojid'] == c.config.sections()


def test_section_error(fixtures_dir):
  c = Config.from_path(f'{fixtures_dir}/kojid-ssl.conf')

  assert {} == c.section('invalid_name')


def test_section_success(fixtures_dir):
  c = Config.from_path(f'{fixtures_dir}/kojid-ssl.conf')

  expected = {
    'maxjobs': '5',
    'use_createrepo_c': 'True',
    'topurl': 'https://koji-hub:8443/pkgs',
    'vendor': 'mbbox',
    'packager': 'mbbox',
    'distribution': 'mbbox',
    'mockhost': 'redhat-linux-gnu',
    'server': 'https://koji-hub:8443/kojihub',
    'build_arch_can_fail': 'True',
    'plugins': '',
    'serverca': '/etc/kojid/certs/ca.pem',
    'cert': '/etc/kojid/certs/cert.pem'
  }

  assert expected == c.section('kojid')  
