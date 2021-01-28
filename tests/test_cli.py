import requests_mock
import koji
import pytest

from koji_builder_kube import cli, errors


def test_session_setup_error_type():
  with pytest.raises(errors.KojiError):
    cli.session_setup({})


def test_session_setup_error_auth(fixtures_dir):
  data = {
    'serverca': f'{fixtures_dir}/ca.pem',
    'cert': f'{fixtures_dir}/cert.pem',
    'server': 'https://koji-hub:8443/koji-hub'
  }
  with pytest.raises(errors.KojiError):
    cli.session_setup(data)


def test_session_setup_success(fixtures_dir, mocker):
  data = {
    'server': 'https://koji-hub:8443/kojihub',
    'serverca': f'{fixtures_dir}/ca.pem',
    'cert': f'{fixtures_dir}/cert.pem',
  }
  mocker.patch('os.access')
  mocker.patch('os.path.exists')
  mocker.patch.object(koji.ClientSession, 'ssl_login', autospec=True)
  cli.session_setup(data)


def test_run_success(fixtures_dir, mocker):
  mocker.patch('os.access')
  mocker.patch('os.path.exists')
  mocker.patch.object(koji.ClientSession, 'ssl_login', autospec=True)
  mocker.patch('koji_builder_kube.cli.mode', cli.Modes.TEST)
  cli.run(['-c', f'{fixtures_dir}/kojid-ssl.conf'])
