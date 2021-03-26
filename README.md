# filetools

- collecting and managing of files metadata
- provide certain statistic about files, directories, grouping information by file extensions
- rename files to use lower case for file extensions
- removing empty files and directories
- removing broken files

## How to use

```bash
$ filetools --help
usage: filetools <command> [<args>]
The list of commands:
    stats       collect statistics about files in the directory
    scan        scan files into the directory for metadata           
    cleanup     removing files, renaming
    info        collect metedata from the file        

positional arguments:
  command               Subcommand to run

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -l LOG_LEVEL, --log_level LOG_LEVEL
                        Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### STATS command

```bash
$ filetools stats --help
usage: filetools [-h] --path PATH [--sort-by {files,size}]

scan files into the directory for metadata

optional arguments:
  -h, --help            show this help message and exit
  --path PATH           the path to the directory for file scanning
  --sort-by {files,size}
                        sort output by number or files or size, default: size
```

Example:
```
General statistics:

| Metric                  | Value    |
|-------------------------|----------|
| Total files             | 22503    |
| Total directories       | 420      |
| Total empty files       | 0        |
| Total empty directories | 0        |
| Total size              | 90.47 GB |

File Extensions statistics:

| Extension   |   Files | Size      |
|-------------|---------|-----------|
| .jpg        |   21558 | 64.15 GB  |
| .mp4        |     262 | 17.06 GB  |
| .avi        |      57 | 4.6 GB    |
| .zip        |      26 | 3.04 GB   |
....

```

### SCAN command

```bash
$ filetools scan --help
usage: filetools [-h] --path PATH [--output-type {jsonline,sqlite3}] [--output-file OUTPUT_FILE] [--ignore-tag IGNORE_TAGS]

scan files into the directory for metadata

optional arguments:
  -h, --help            show this help message and exit
  --path PATH           the path to the directory for file scanning
  --output-type {jsonline,sqlite3}
                        the output type
  --output-file OUTPUT_FILE
                        the path output file for storing metadata
  --ignore-tag IGNORE_TAGS
                        the tags for ignoring
```

### CLEANUP command

**NOTE! Be very careful with this command, all actions are on your risk**

```bash
$ filetools cleanup --help
usage: filetools [-h] --path PATH [--use-lower-case-in-file-ext] [--remove-broken-files] [--remove-empty-files] [--remove-empty-directories] [--force]

scan files into the directory for metadata

optional arguments:
  -h, --help            show this help message and exit
  --path PATH           the path to the directory for file scanning
  --use-lower-case-in-file-ext
                        use lower case in file extensions, default: False
  --remove-broken-files
                        remove broken files
  --remove-empty-files  remove empty files
  --remove-empty-directories
                        remove empty directories
  --force               apply forced action, default: False
```