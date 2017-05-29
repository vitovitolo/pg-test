#!/usr/bin/python

import random
import string
import optparse
import pg
import threading
import math
from multiprocessing.dummy import Pool as ThreadPool

MAX_DB_CONNS = 99

def get_random_string(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

def insert_rows(db, table, insert_id):
    f_name=get_random_string(10)
    pg.query('INSERT INTO {} (id, name) \
              VALUES ( \'{}\', \'{}\')'.format(table, insert_id, f_name), db)

def create_tables(db_table):
    db = db_table[0]
    table = db_table[1]
    pg.query('CREATE TABLE IF NOT EXISTS {} \
              ( id integer NOT NULL,\
               name varchar(20) NOT NULL,\
               PRIMARY KEY (id) ) ;'.format(table), database=db)
    for i in range(10):
        insert_rows(db, table, i)

def create_database(tables_db):
    tables = tables_db[0]
    db = tables_db[1]
    pg.query('CREATE DATABASE {}'.format(db))

    table_list = []
    for i in range(tables):
       table_list.append((db,get_random_string(10)))
    
    pool = ThreadPool(int(math.sqrt(MAX_DB_CONNS)))
    result = pool.map(create_tables, table_list)
    pool.close()
    pool.join()

def populate_all(databases, tables, rows):
    db_list = []
    for i in range(databases):
       db_list.append((tables,get_random_string(10)))
    pool = ThreadPool(int(math.sqrt(MAX_DB_CONNS)))
    result = pool.map(create_database, db_list)
    pool.close()
    pool.join()

if __name__ == "__main__":
    PROGRAM_NAME = str(__file__)
    parser = optparse.OptionParser("usage: " + PROGRAM_NAME + 
                                   " --databases 10 --tables 10 ")
    parser.add_option("-d", "--databases", \
                      dest="databases", \
                      type="int", \
                      default=10, \
                      help="Number of database to create")
    parser.add_option("-t", "--tables", \
                      dest="tables", \
                      type="int", \
                      default=10, \
                      help="Number of tables to create in each database")
    parser.add_option("-r", "--rows", \
                      dest="rows", \
                      type="int", \
                      default=10, \
                      help="Number of max rows to create in each table.")


    (options, args) = parser.parse_args()

    populate_all(databases=options.databases, \
                 tables=options.tables, \
                 rows=options.rows)
