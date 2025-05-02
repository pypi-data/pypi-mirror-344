from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='zamzar-sdk',
    version='1.0.2',
    install_requires=['zamzar'],
    py_modules=['zamzar_sdk'],
    description='Deprecated: please use the zamzar package instead',
    long_description=long_description,
    long_description_content_type="text/markdown",
)