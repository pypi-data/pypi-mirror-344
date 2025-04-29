from setuptools import setup, find_packages

setup(
    name="pytest-gradescope",
    version="0.1.0",
    description="A pytest plugin for Gradescope integration",

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
