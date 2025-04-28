from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pinetodo",
    version="1.0.1",
    description="`PineToDo` is a tool with [CLI](https://id.wikipedia.org/wiki/Command_Line_Interface) or `Command_Line_Interface` based, designed to create and manage tasks in todo style",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="openpineaplehub",
    author_email="openpineaple@gmail.com",
    url="https://github.com/openpineapletools/pinetodo",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
         "json5",
        "requests",
        "rich",
    ],  
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ],
    entry_points={
        "console_scripts": [
            "pinetodo=pinetodo.main:main", 
        ],
    },
    project_urls={
        "Bug Tracker": "https://github.com/openpineapletools/pinetodo/issues",
        "Request Features": "https://github.com/openpineapletools/pinetodo/pulls",
        "Documentation Pinetodo": "https://openpineapletools.github.io/pinetodo/#/"
    },
)
