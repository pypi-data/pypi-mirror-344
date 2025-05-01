from setuptools import setup, find_packages

setup(
    name="pb_checker",
    version="1.0.1",  # Naikkan versi
    packages=find_packages(),
    install_requires=[
        "requests>=2.26.0",
        "beautifulsoup4>=4.9.3",
        "colorama>=0.4.4"
    ],
    entry_points={
        'console_scripts': [
            'pb-checker=pb_checker.pb:main',
        ],
    },
)