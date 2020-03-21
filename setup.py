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
  package_data={"pylightnix": ["py.typed"]},
  zip_safe=False, # https://mypy.readthedocs.io/en/latest/installed_packages.html
  version="0.1.0",
  author="grwlf",
  author_email="grrwlf@gmail.com",
  description="A Nix-style datastore management library in Python",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/stagedml/pylightnix",
  packages=find_packages(where='src'),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: POSIX :: Linux",
    "Topic :: System :: Software Distribution",
    "Topic :: Software Development :: Build Tools",
    "Intended Audience :: Developers",
    "Development Status :: 3 - Alpha",
  ],
  python_requires='>=3.6',
  test_suite='pytest',
  tests_require=['pytest', 'pytest-mypy', 'hypothesis'],
)


