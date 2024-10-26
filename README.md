# Tidyup 🧹

> Sweep up your files into organized piles for clean up  

## Description  

Simple python utility to clean up project directories from the mess you make while working.  

### How it works  

Go to the directory, get all of the files, exclude the ones that are likely important for your project and then create directories in the project by the file extension. Once the directory is made, the files are moved to the file extension directory.

## Usage

Install the python utility:

```bash
pip install tidyup
```

Then get to tidying up 


```bash
#Clean up directory with the structure year/month/extension/file_here.extension
tidyup -de <directory/with/mess>
```

## Functionality

```bash

tidyup -h
usage: tidyup [-h] [-e] [-d] directory

Organize files by extension and/or date.

positional arguments:
  directory   Directory to organize

options:
  -h, --help  show this help message and exit
  -e          Organize by extension
  -d          Organize by date

Examples:
  tidyup -e /path/to/dir       Organize by extension
  tidyup -d /path/to/dir       Organize by date
  tidyup -ed /path/to/dir      Organize by extension and date
  tidyup -de /path/to/dir      Organize by date and extension
```



