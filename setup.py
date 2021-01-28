# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = ''

setup(
    long_description=readme,
    name='koji-builder-kube',
    version='0.1.0',
    python_requires='==3.*,>=3.6.0',
    author='lrossett',
    author_email='lrossett@redhat.com',
    entry_points={"console_scripts": ["kojid = koji_builder_kube.cli:main"]},
    packages=['koji_builder_kube', 'koji_builder_kube.session'],
    package_dir={"": "src"},
    package_data={},
    install_requires=[
        'koji==1.*,>=1.23.1', 'mypy==0.*,>=0.790.0', 'requests==2.*,>=2.25.1',
        'typing==3.*,>=3.7.4', 'typing-extensions==3.*,>=3.7.4'
    ],
    extras_require={
        "dev": [
            "pytest==5.*,>=5.2.0", "pytest-mock==3.*,>=3.5.1",
            "requests-mock==1.*,>=1.8.0", "sphinx==3.*,>=3.4.3",
            "sphinx-rtd-theme==0.*,>=0.5.1"
        ]
    },
)