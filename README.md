# Broom 🧹

> Sweep up your files into organized piles for clean up  

## Description  

Simple python utility to clean up project directories from the mess you make while working.  

### How it works  

Go to the directory, get all of the files, exclude the ones that are likely important for your project and then create directories in the project by the file extension. Once the directory is made, the files are moved to the file extension directory.

## Usage

Clone the repo, go to the directory and use the python utility:

```bash
git clone git@github.com:Esturban/broom.git
cd broom
python broom.py <directory/with/mess>
```

