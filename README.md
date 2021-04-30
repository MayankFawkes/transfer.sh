[![banner](https://github.com/MayankFawkes/transfer.sh/raw/master/img/transfer.png)](https://github.com/MayankFawkes/transfer.sh)

[![Publish to PyPI](https://github.com/MayankFawkes/transfer.sh/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/MayankFawkes/transfer.sh/actions/workflows/pypi-publish.yml)
![ver](https://img.shields.io/pypi/pyversions/transfer.sh)
![lang](https://img.shields.io/github/languages/top/mayankfawkes/transfer.sh)
![status](https://img.shields.io/pypi/status/transfer.sh)
![ver](https://img.shields.io/pypi/v/transfer.sh)
[![Downloads](https://pepy.tech/badge/transfer.sh/week)](https://pepy.tech/project/transfer-sh)

# transfer.sh
Transfer.sh command line program, Now file sharing from the command line.

# Installation
One command installation

## With Python
run commands on terminal.

```
$ pip install -U transfer.sh
```

Have multipls versions of python?

```
$ python3.x -m pip install -U transfer.sh
```
## Linux
```
$ curl --silent "https://api.github.com/repos/MayankFawkes/transfer.sh/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/' | { tag=($(< /dev/stdin)); sudo curl -L "https://github.com/MayankFawkes/transfer.sh/releases/download/$tag/transfer" -o /usr/local/bin/transfer; sudo chmod +x /usr/local/bin/transfer;}
```

# CLI
Command line help

## Upload file
```
$ transfer upload file.txt
```
## Remove file
```
$ transfer remove <uploaded file hash>
```
## List uploaded files
```
$ transfer list --show
```
