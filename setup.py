import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="transfer.sh",
    version="1.0.0",
    description="unofficial transfer.sh CLI",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mayankfawkes",
    author="Mayank Gupta",
    author_email="mayankfawkes@gmail.com",
    license="MIT License",
    project_urls={
            "Documentation": "https://github.com/mayankfawkes",
            "Source": "https://github.com/mayankfawkes",
        },
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        'Topic :: System :: Networking',
        'Topic :: Internet :: WWW/HTTP',
        "Natural Language :: English",
        'Environment :: Plugins',
        "Environment :: Console",
        "Topic :: Terminals",
        "Topic :: Utilities",
        ],

    packages=["transfer"],
    python_requires=">=3.6",
    keywords=[],
    include_package_data=True,
    install_requires=[],
)
