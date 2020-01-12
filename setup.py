from setuptools import setup, find_packages

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
  name="pylightnix",
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


