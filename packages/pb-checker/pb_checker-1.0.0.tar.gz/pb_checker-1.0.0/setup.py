from setuptools import setup, find_packages

setup(
    name="pb_checker",
    version="1.0.0",
    author="Masanto",
    author_email="haninkazugawa@gmail.com",
    description="Library untuk mengecek akun Point Blank",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)