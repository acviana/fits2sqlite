fits2sqlite
===========

A tool for exporting header data from astronomy FITS images in a SQLIte database.

Description
-----------
fits2sqlite is a lightweight python tool created to allow astronomers to easily  store header information from FITS files using the SQLite relational database standard.

Motivation
----------

In progress.



Usage
-----

`> python fits2sqlite.py  --files 'data/*.fits' --database 'headers.db' [--verbose]`

Dependencies
------------
SQLite [http://www.sqlite.org/]

Python:
 - argparse
 - glob
 - os
 - pyfits
 - sqlite3

Future Work
-----------

 - Currently only data from the 0th header is read.