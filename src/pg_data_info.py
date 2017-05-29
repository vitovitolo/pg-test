#!/usr/bin/python

import pg

def get_size_db(db_name):
   """
   Return the size of the data of a given database.
   This query only check the data of all tables excluding indexes data
   If something goes wrong, return 0
   """
   status, result_list = pg.query("SELECT SUM(pg_table_size(c.oid)) \
                                   FROM pg_class c \
                                   JOIN pg_database d ON d.datdba = c.relowner \
                                   WHERE c.relkind = 'r' \
                                   AND d.datname = \'{}\';".format(db_name), db_name)
   if status:
      return result_list[0][0]
   else:
      return 0

def get_size_all_dbs():
   """
   Get the size of all databases. Connect to each db and retrieve size of it.
   Return a dict with the database as the key and the size as the value
   """
   all_dbs = pg.get_all_dbs()
   size_all_dbs = {}
   for db in all_dbs:
      size_all_dbs[db] = get_size_db(db)
   return size_all_dbs

def get_percentile(percentile, list_ordered):
   """
   Function to calculate percentile of a previous ordered list.
   Get the index element mutiplying percentile by number of elements.
   If the index is a whole number, get the list[index] element
   and the percentile is the average of that element and the next one in order;
   if not, round it up to the nearest whole number and get list[round]
   """
   if not list_ordered:
      return 0

   index = percentile * len(list_ordered)
   if index.is_integer():
      percentile90 = ( list_ordered[int(index-1)] + list_ordered[int(index)] ) / 2 
   else:
      percentile90 = list_ordered[int(round(index,0))-1]
   return percentile90

if __name__ == "__main__":
   """
   Main logic of the program that retrieve some data info from a postgresql.
   Calculates the size of each database and excluding indexes.
   Print the total size of the whole databases.
   Print the average of database data.
   Calculate the percentile 90 of the database size list and print it.
   """
   dict_all_dbs_size = get_size_all_dbs()
   total_size = 0
   for db, size in dict_all_dbs_size.iteritems():
      if size:
         total_size += int(size)
   print "Total size across the entire database server: {} bytes".format(total_size)
   if len(dict_all_dbs_size):
      average_size = total_size / len(dict_all_dbs_size)
   else:
      average_size = 0
   print "Average size of databases\' data: {} bytes".format(average_size)
   # Order the database list by size
   list_ordered = []
   for size in sorted(dict_all_dbs_size, key=dict_all_dbs_size.get):
      list_ordered.append(dict_all_dbs_size[size])
   percentile90 = get_percentile(0.90, list_ordered)
   print "Percentile 90 of databases\' data: {} bytes".format(percentile90)
