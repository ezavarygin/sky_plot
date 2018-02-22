# README

## Description

To be added...

## Requirements
The software was written to work with `python 3`. 

**Python modules used:**

- mpl_toolkits
- matplotlib
- astropy
- numpy
- sys


## Usage

`python sky_plot.py file_with_coordinates.txt [--option]`

Options:
```
--gal - coordinates in file_with_coordinates.txt are l and b galactic coordinates. 

--eq  - coordinates in file_with_coordinates.txt are RA and DEC equatorical coordinates.

One of the two options above must be specified.

--ham - Use [Hammer](https://matplotlib.org/basemap/users/hammer.html) projection. Otherwise, [Mollweide](https://matplotlib.org/basemap/users/moll.html) projection is used.
```
