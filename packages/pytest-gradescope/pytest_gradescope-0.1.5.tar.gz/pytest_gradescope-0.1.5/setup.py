from setuptools import setup, find_packages

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="pytest-gradescope",
    version="0.1.5",
    description="A pytest plugin for Gradescope integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sebastian Ingino",
    author_email="sebastian@ingino.me",
    license="MIT",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    # the following makes a plugin available to pytest
    entry_points={
        "pytest11": [
            "pytest-gradescope = pytest_gradescope.pytest_plugin",
        ]
    },
    # custom PyPI classifier for pytest plugins
    classifiers=[
        "Framework :: Pytest",
    ],
)
