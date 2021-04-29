import pathlib
from setuptools import setup
from transfer import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="transfer.sh",
    version=f"{__version__}",
    description="transfer.sh CLI",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MayankFawkes/transfer.sh",
    author="Mayank Gupta",
    author_email="mayankfawkes@gmail.com",
    license="MIT License",
    project_urls={
            "Documentation": "https://github.com/MayankFawkes/transfer.sh/blob/master/README.md",
            "Source": "https://github.com/MayankFawkes/transfer.sh",
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
    entry_points={
        "console_scripts": ["transfer = transfer.cli:main"],
        },
    packages=["transfer"],
    python_requires=">=3.6",
    keywords=["upload", "cli", "transfer.sh"],
    include_package_data=True,
    install_requires=["requests"],
)
