#!/usr/bin/env python3

from setuptools import setup, find_packages

# Read the contents of README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="inquisitor-search",
    version="1.0.0",
    author="V. Oliver Walsh",
    author_email="oliverwalsh7@gmail.com",
    description="Get real-time, cited answers from the web with intelligent caching",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vowalsh/inquisitor-search",
    py_modules=[
        "inquisitor",
        "cache", 
        "search",
        "llm",
        "formatting"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "inquisitor=inquisitor:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
