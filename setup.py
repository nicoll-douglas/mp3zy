from setuptools import setup, find_packages

setup(
  name="mp3zy",
  version="0.1.0",
  packages=find_packages(where="backend"),
  package_dir={"": "backend"},
)
