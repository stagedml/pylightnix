from setuptools import setup, find_packages
from os import environ
from os.path import isfile

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
  name="pylightnix",
  package_dir={'':'src'},
  package_data={"pylightnix": ["py.typed"]},
  zip_safe=False, # https://mypy.readthedocs.io/en/latest/installed_packages.html
  use_scm_version=True,
  author="grwlf",
  author_email="grrwlf@gmail.com",
  description="A Nix-style immutable data management library in Python",
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
  setup_requires=['setuptools_scm'],
)


