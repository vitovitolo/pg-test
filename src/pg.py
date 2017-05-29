#!/usr/bin/python

import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
sys.path.append('/opt/pg_scripts/conf')
import config

def query(query_string, database=config.DEFAULT_DB):
   """
   Execute a query given by param and return True/False and result.
   result is a list of tuples with the query output info
   """
   status = True
   try:
      conn = psycopg2.connect(user=config.USERNAME, \
                              password=config.PASSWD, \
                              database=database, \
                              host=config.HOST, \
                              connect_timeout=3)
      conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
   except psycopg2.OperationalError as e:
      print "Error connecting to postgresql: {}".format(e)
      return False, []

   try:
      cur = conn.cursor()
      cur.execute(query_string)
   except psycopg2.Error as e:
      print "Error executing query: {}".format(e)
      return False, []

   #Catch this error due to weird behaviour in psycopg2
   #when CREATE DATABASE is fetched
   try:
      result = cur.fetchall()
   except psycopg2.ProgrammingError as e:
      return True, []

   cur.close()
   conn.close()
   return status, result

def get_all_dbs(database=config.DEFAULT_DB):
   """
   Function to retrieve a list with all db names from postgresql
   Returns an empty list if something goes wrong
   """
   status,result_list = query('SELECT datname \
                               FROM pg_stat_database \
                               WHERE datname <> \'template0\' \
                               AND datname <> \'template1\' \
                               AND datname <> \'postgres\' ;')
   if status:
      # convert from list of tuples to list of elements
      result = []
      for elem in result_list:
         result.append(elem[0])
      return result
   else:
      return []
