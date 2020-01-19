from setuptools import setup, find_packages
from distutils.spawn import find_executable

with open("README.md", "r") as fh:
  long_description = fh.read()

WGET=find_executable('wget')
assert WGET is not None, '`wget` executable not found. Please install system package `wget` and check PATH'

AUNPACK=find_executable('aunpack')
assert AUNPACK is not None, '`aunpack` executable not found. Please install system package `atool` and check PATH'

SHA256SUM=find_executable('sha256sum')
assert SHA256SUM is not None, '`sha256sum` executable not found. It should be in `coreutils` system package, please figure out why is it missing. Check PATH.'

setup(
  name="pylightnix",
  package_dir={'':'src'},
  version="0.0.1",
  author="grwlf",
  author_email="grrwlf@gmail.com",
  description="A Nix-styled datastore management library in Python",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/stagedml/pylightnix",
  packages=find_packages(where='src'),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
  test_suite='pytest',
  tests_require=['hypothesis', 'pytest-mypy'],
)


