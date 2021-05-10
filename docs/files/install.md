# Installation
One command installation

## Python
run commands on terminal.

```
$ pip install -U transfer.sh
```

Have multipls versions of python?

```
$ python3.x -m pip install -U transfer.sh
```
## Linux

### AMD64 
```
$ curl --silent "https://api.github.com/repos/MayankFawkes/transfer.sh/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/' | { tag=($(< /dev/stdin)); sudo curl -L "https://github.com/MayankFawkes/transfer.sh/releases/download/$tag/transfer-linux-amd64" -o /usr/local/bin/transfer; sudo chmod +x /usr/local/bin/transfer;}
```

### i386
```
$ curl --silent "https://api.github.com/repos/MayankFawkes/transfer.sh/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/' | { tag=($(< /dev/stdin)); sudo curl -L "https://github.com/MayankFawkes/transfer.sh/releases/download/$tag/transfer-linux-i386" -o /usr/local/bin/transfer; sudo chmod +x /usr/local/bin/transfer;}
```
