import os
from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name = "builder",
    version = "0.0.1",
    author = "Theodoros Mavroeidakos",
    description = ("A tool automating operations with docker containers"),
    py_modules=["builder"],
    python_requires='>=3.7',
    install_requires=['docker', 'Click', 'requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: Alpha",
        "Topic :: Docker Utilities",
    ],
    entry_points='''
        [console_scripts]
        builder=builder:cli
    ''',

    project_urls={
    'Docker Project': 'https://github.com/tmavroeid/docker-project',

},
)
