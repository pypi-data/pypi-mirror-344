from setuptools import setup, find_packages

setup(
    name="pb_checker",
    version="1.0.2",
    packages=find_packages(),
    install_requires=[
        'requests>=2.26.0',
        'beautifulsoup4>=4.9.3'
    ],
)