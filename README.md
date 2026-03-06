# Tidyup 🧹

> Sweep up your files into organized folders by date and/or extension.

## Description

`tidyup` helps organize messy directories by moving eligible files into a predictable
folder structure.

## Install

```bash
pip install tidyup
```

## Usage

```bash
tidyup [-h] [-e] [-d] [-r] [-L DEPTH] directory
```

### Options

- `-e`: organize by extension
- `-d`: organize by file modified date (`year/month`)
- `-r, --rearrange`: traverse subdirectories recursively
- `-L, --depth`: recursion depth (valid only with `-r`)

### Ordering Behavior

Order is preserved:

- `-de` => `year/month/extension/file`
- `-ed` => `extension/year/month/file`

### Recursive Behavior

- `-r` without `-L` defaults to depth `2`
- `-L` without `-r` is invalid

### Exclusion Behavior

By default, tidyup excludes:

- hidden files (dotfiles)
- names/suffixes in the internal exclusion list (for example `requirements.txt`, `config.json`)
- files without an extension
- multi-extension files are grouped by their final suffix (for example `archive.tar.gz` goes to `gz/`)

### Collision Behavior

- tidyup never overwrites an existing destination file
- if a destination filename already exists, that move is skipped and a message is printed
- when multiple source files would target the same destination in one run, tidyup processes them in a stable path order so the outcome stays deterministic

### Examples

```bash
# Organize top-level files by extension
tidyup -e /path/to/dir

# Organize top-level files by date
tidyup -d /path/to/dir

# Organize by extension then date
tidyup -ed /path/to/dir

# Organize by date then extension
tidyup -de /path/to/dir

# Recursive organize by date, default depth=2
tidyup -r -d /path/to/dir

# Recursive organize by extension, default depth=2
tidyup -r -e /path/to/dir

# Recursive organize by extension at depth 3
tidyup -r -L 3 -e /path/to/dir

# Recursive organize by date at depth 3
tidyup -r -L 3 -d /path/to/dir
```
