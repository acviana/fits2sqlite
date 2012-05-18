#! /usr/bin/env python
'''
A Python module for inserting FITS header data in a SQLite database.

Command line help available by running:
> python fits2sqlite -h

Alex C. Viana
alex.costa.viana@gmail.com
'''

import argparse
import glob
import os
import pyfits
import sqlite3

# -----------------------------------------------------------------------------
# Functions (alphabetical)
# -----------------------------------------------------------------------------

def get_id(database,filename):
    '''
    Return the id of the that matches that filename. Return [] if 
    there is no match. Raise AssertionError if there is more than
    one match.
    '''
    conn = sqlite3.connect(database)
    c = conn.cursor()
    command = 'SELECT id FROM headers WHERE filename = "' 
    command += os.path.basename(filename) + '"'
    c.execute(command)
    id = c.fetchall()
    conn.close()
    
    assert len(id) in [0,1], 'Multiple rows match filename.'
    return id

# -----------------------------------------------------------------------------

def get_file_list(search_string):
    '''
    Get the file list based on the seach string.
    '''
    search_string = os.path.abspath(search_string)
    print search_string
    file_list = glob.glob(search_string)
    
    assert file_list != [], 'No files found.'
    return file_list

# -----------------------------------------------------------------------------

def get_header(filename):
    '''
    Get the header information.
    '''
    f = pyfits.open(filename)
    header = f[0].header
    f.close()
    header.update('filename', os.path.basename(filename))
    
    return header
    
# -----------------------------------------------------------------------------

def ingest_header(args,filename):
    '''
    Ingest the header information with an UPDATE or INSERT.
    '''
    if args.verbose == True:
        print filename
    header = get_header(filename)
    id = get_id(args.database, filename)
    if id == []:
        insert_header(args.database, header)
    else:
        update_header(args.database, header, id)

# -----------------------------------------------------------------------------

def insert_header(database,header):
    '''
    Insert the header information into the database.
    '''
    conn = sqlite3.connect(database)
    c = conn.cursor()
    command = 'INSERT INTO headers ('
    for key in header:
        command += '"' + key +'",'
    command = command[:-1]
    command += ') VALUES ('
    for key in header:
        command += '"' + str(header[key]) + '",'
    command = command[:-1]
    command += ')'
    c.execute(command)
    conn.commit()
    conn.close()

# -----------------------------------------------------------------------------

def make_header_set(file_list):
    '''
    Returns all the header keywords as a set object.
    '''
    header_set = set()
    for filename in file_list:
        header = get_header(filename)
        for key in header.iterkeys():
            header_set.add(key)
            
    return header_set

# ------------------------------------------------------------------------------

def make_table(database):
    '''
    Run the schema.
    '''
    conn = sqlite3.connect(database)
    c = conn.cursor()
    
    sql = open('makefitsdb.sql').read()
    c.executescript(sql)

    conn.commit()
    conn.close()
    
# ------------------------------------------------------------------------------

def prase_args():
    '''
    Prase the command line arguemnts.
    '''
    parser = argparse.ArgumentParser(
        description = 'Inserts FITS header information in a SQLite database.' )
    parser.add_argument(
        '--files', 
        required = True,
        help = 'Search string for the fits files you want to ingest.\
            e.g. "dir/*.fits"')
    parser.add_argument(
        '--database',
        required = True,
        help = 'Path to the SQLite database.')
    parser.add_argument(
        '--verbose',
        required = False,
        type = bool,
        default = False,
        help = 'Print steps')
    args = parser.parse_args()
        
    return args

# -----------------------------------------------------------------------------

def update_header(database,header,id):
    '''
    Update the header information for an already existing row.
    '''
    conn = sqlite3.connect(database)
    c = conn.cursor()
    command = 'UPDATE OR ROLLBACK headers SET '
    for key in header:
        command += '"' + key + '" = "' + str(header[key]) + '",'
    command = command[:-1]
    command += ' WHERE id = "' + str(id[0][0]) + '"'
    c.execute(command)
    conn.commit()
    conn.close()
    
# ------------------------------------------------------------------------------
    
def write_table_schema(header_set):
    '''
    Create the SQLite schema for the table.
    '''
    f = open('makefitsdb.sql','w')
    f.write('BEGIN;\n')
    f.write('CREATE TABLE IF NOT EXISTS headers (\n')
    f.write('\tid INTEGER PRIMARY KEY,\n')
    #f.write('\tfilename TEXT UNIQUE ON CONFLICT REPLACE,\n')
    while len(header_set) > 1:
        f.write('\t "' + header_set.pop() + '" TEXT,\n')
    else:
        f.write('\t "' + header_set.pop() + '" TEXT\n')
    f.write(');\n')
    f.write('COMMIT;\n')
    f.close()
    
# -----------------------------------------------------------------------------
# The main controller. 
# -----------------------------------------------------------------------------

def main(args):
    '''
    The mail controller. 
    '''
    file_list = get_file_list(args.files)
    database_test = os.access(args.database,os.F_OK)
    if database_test == False:
        header_set = make_header_set(file_list)
        write_table_schema(header_set)
        make_table(args.database)
    
    for filename in file_list:
        ingest_header(args,filename)

# -----------------------------------------------------------------------------
# For command line execution.
# -----------------------------------------------------------------------------


if __name__ == '__main__':
    args = prase_args()
    main(args)
