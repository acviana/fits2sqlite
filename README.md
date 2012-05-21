fits2sqlite
===========

A tool for exporting header data from astronomy FITS images in a SQLIte database.

Description
-----------
fits2sqlite is a lightweight python command line tool that exports header information from FITS files into a SQLite database.

Astronomy images in the FITS format contain image metadata (data about the data) in the header of each extension. However, this information is tied up in each individual image making it difficult to sort and query images from large datasets. 

fits2sqlite solves this problem by consolidates header information in a SQLite database. SQLite is a self-contained serverless relational database that offers many advantages over flat-files. 

Features
--------

 - If the SQLite database specified does not exist it will be created.
 - Each header keyword will be a separate field in a table called headers.
 - A unique integer id is created for each file name.
 - Each field (except for the id field) will be a text type.
 - The file name field has a uniqueness contraint. 
 - If a file is ingested that already exists in the database the header information is updated.

Usage
-----

For help:
`> python fits2sqlite.py -h`

To Run:
`> python fits2sqlite.py  --files 'data/*.fits' --database 'headers.db' [--verbose]`

Dependencies
------------
SQLite [http://www.sqlite.org/]

Python (all part of the python standard library):
 - argparse
 - glob
 - os
 - pyfits
 - sqlite3
