import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="swimlane_environment_validator",
    version="1.0.0",
    description="swimlane_environment_validator",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://swimlane.com",
    author="Swimlane",
    author_email="info@swimlane.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
    packages=["swimlane_environment_validator", "swimlane_environment_validator.lib"],
    include_package_data=True,
    install_requires=[
        "requests",
        "pyOpenSSL"
    ],
    entry_points={
        "console_scripts": [
            "swimlane_environment_validator=swimlane_environment_validator.__main__:main",
        ]
    },
)
