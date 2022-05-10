# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name="football-elo",
    version="1.0.0",
    author="Alexander Malko",
    author_email="",
    description="Package provides backend tools for football matches arrangement via telegram bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/A1ema1k/alemalk",
    project_urls={
        "Bug Tracker": "https://github.com/A1ema1k/alemalk/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(include="football_elo"),
    install_requires=[
        'pytelegrambotapi',
        'pandas'
    ],
    test_suite="tests",
    python_requires=">=3.7",
)