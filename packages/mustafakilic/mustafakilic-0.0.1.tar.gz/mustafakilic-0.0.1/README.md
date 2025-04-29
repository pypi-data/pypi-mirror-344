# Project description
### Make sure you have upgraded version of pip

Windows
```
py -m pip install --upgrade pip
```
Linux/MAC OS
```
python3 -m pip install --upgrade pip
```

## Create a project with the following structure
```
packaging_tutorial/
├── dist
├── src/
│   └── example_package/
│       ├── __init__.py
│       └── example.py
│
├── tests/
│    └── test_example.py
│
├── LICENSE
├── pyproject.toml
└── README.md

mkdir dist
mkdir src/example_package
touch src/example_package/__init__.py
touch src/example_package/example.py
mkdir tests
touch tests/test_example.py
touch LICENSE
touch pyproject.toml
```

## pyproject.toml
This file tells tools like pip and build how to create your project

```
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "example-pkg-YOUR-USERNAME-HERE"
version = "0.0.1"
authors = [
    { name = "Example Author", email = "author@example.com" },
]
description = "A small example package"
readme = "README.md"
keywords = ["key1", "key2"]
requires-python = ">=3.10"
classifiers = [

    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
]

[project.urls]
Homepage = "https://github.com/pypa/sampleproject"
```
build-system.requires gives a list of packages that are needed to build your package. Listing something here will only make it available during the build, not after it is installed.

build-system.build-backend is the name of Python object that will be used to perform the build. If you were to use a different build system, such as flit or poetry, those would go here, and the configuration details would be completely different than the setuptools configuration described below.

## Running the build
### Make sure your build tool is up to date

Windows
```
py -m pip install --upgrade build
```

Linux/MAC OS
```
python3 -m pip install --upgrade build
```

### Create the build
```
py -m build
```

### References
https://packaging.python.org/tutorials/packaging-projects/