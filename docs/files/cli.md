# CLI
Command line help
```
usage: transfer [-h] [-V] Options ...

transfer.sh CLI

optional arguments:
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit

Required Options:
  Options        Help
    remove (rm)  Remove uploaded file.
    upload (up)  Upload file.
    list (l)     Manage all uploaded files.
```

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