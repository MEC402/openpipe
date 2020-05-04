import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="openpiPy",
    version="0.0.0",
    description="OpenPipe is an open source federated content production pipeline this is lightweight and extensible.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MEC402/openpipe",
    author="Openpipe Team",
    # author_email="office@realpython.com",
    # license="MIT",
    classifiers=[
        # "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["backend/openpipeAPI"],
    include_package_data=True,
    # install_requires=["feedparser", "html2text"],
    # entry_points={
    #     "console_scripts": [
    #         "realpython=reader.__main__:main",
    #     ]
    # },
)