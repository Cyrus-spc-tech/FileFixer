from setuptools import setup, find_packages

setup(
    name="filefix",
    author="",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        'typer'
    ],
    description="A CLI toolkit to organize files effectively.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Cyrus-spc-tech/FileFixer.git",
)
