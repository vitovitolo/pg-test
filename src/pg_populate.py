#!/usr/bin/python

import random
import string
import optparse
import pg
import threading


def get_random_string(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

def insert_rows(db, table, insert_id):
    f_name=get_random_string(10)
    pg.query('INSERT INTO {} (id, name) \
              VALUES ( \'{}\', \'{}\')'.format(table, insert_id, f_name), db)

def create_table(db, rows):
    table=get_random_string(10)
    pg.query('CREATE TABLE IF NOT EXISTS {} \
              ( id integer NOT NULL,\
               name varchar(20) NOT NULL,\
               PRIMARY KEY (id) ) ;'.format(table), database=db)
    for i in range(rows):
       insert_rows(db, table, i)

def create_database(tables, rows):
    db=get_random_string(10)
    pg.query('CREATE DATABASE {}'.format(db))
    table_threads = list()
    for i in range(tables):
        t = threading.Thread(target=create_table, args=(db, rows))
        table_threads.append(t)
        t.start()

def populate_all(databases, tables, rows):
    db_threads = list()
    for i in range(databases):
        t = threading.Thread(target=create_database, args=(tables, rows))
        db_threads.append(t)
        t.start()

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
