# Blaseball Notebooks

Various python scripts and Jupyter Notebooks for Blaseball things.

Blaseball is No More, so no guarantee any of this still runs

https://edgarware.github.io/blaseball_notebooks/

## Running Locally
If running Python 3.8+
```shell
pip install jupyter
pip install -r requirements.txt
jupyter notebook
```

## Generating HTML
Requires Jupyter 6.0+
```shell
python nb_build.py
```
Output files will be in `docs/`

## OK but for real how does this work
Jupyter Notebooks are used to perform analysis in Python. There's a bunch of python
files with additional blaseball-specific functions to make this easier, you can see
the tutorial for examples of some of these. Then after a file is run the whole file
gets pushed to this repository.

Then GitHub Actions runs the included `nb_build.py` script to use nbconvert and make
static HTML files for each notebook. Then it pushes it up to GitHub pages and tada!
You have a bunch of webpages, automatically deployed.

### How do I use it for my own stuff?
First step is to fork the repository. Then you can modify anything you want, delete files,
make it your own. When you want stuff to get pushed up to a website, head to your
repository's settings and configure GitHub Pages, specifically for automatic upload. It
should auto-push any time you modify a notebook.

You will also likely want to modify the nb_build.py script a bit, it's pretty specialized
for my site and repository structure. I don't really have notes on this one, just poke
around and see what happens.
