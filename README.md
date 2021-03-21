# filetools

Tools for collecting and managing of files metadata


## How to use

```bash
$ filetools --help
usage: filetools <command> [<args>]
The list of commands:
    stats       collect statistics about files in the directory
    scan        scan files into the directory for metadata
    info        collect metedata from the file
    normalize   normalize filenames

positional arguments:
  command               Subcommand to run

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -l LOG_LEVEL, --log_level LOG_LEVEL
                        Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Collect statistics

```bash
$ filetools stats --help
usage: filetools [-h] -d PATH

scan files into the directory for metadata

optional arguments:
  -h, --help            show this help message and exit
  -d PATH, --directory PATH
                        the path to the directory for file scanning

```

### Scan directory

```bash
$ filetools scan --help
usage: filetools [-h] --path PATH [--output-type {jsonline,sqlite3}] [--output-file OUTPUT_FILE] [--ignore-tag IGNORE_TAGS]

scan files into the directory for metadata

optional arguments:
  -h, --help            show this help message and exit
  --path PATH           the path to the directory for file scanning
  --output-type {jsonline,sqlite3}
                        the output type, possible options: jsonline or sqlite3
  --output-file OUTPUT_FILE
                        the path output file for storing metadata
  --ignore-tag IGNORE_TAGS
                        the tags for ignoring
```

### Normalize filenames

```bash
$ filetools normalize --help
usage: filetools [-h] -d PATH

scan files into the directory for metadata

optional arguments:
  -h, --help            show this help message and exit
  -d PATH, --directory PATH
                        the path to the directory for file scanning
```