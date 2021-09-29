import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="sduiapi",
    version="1.0.0",
    description="A script, to fetch data from sdui, and return it as a python dict",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/AnnikenYt/SduiAPI",
    author="@Bigboy32&@AnnikenYT",
    author_email="cenec.dev@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["sduiapi"],
    include_package_data=True,
    install_requires=["colorama", "requests"],
)