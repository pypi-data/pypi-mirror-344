from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="gadutils",
    version="0.0.3",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={},
    author="Alexander Grishchenko",
    author_email="alexanderdemure@gmail.com",
    description="A lightweight utility library for building clean and reusable data manipulation functions.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AlexDemure/gadutils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
