#!/usr/bin/python

import os
import sys
import optparse
import subprocess
import pg

def dbs_under_threshold(min_dbs=1):
    """
    Check if number of databases are below threshold given by parameter
    return True if everything is ok
    return False if are under threshold or there was an error
    """
    list_dbs = pg.get_all_dbs()
    if len(list_dbs) < min_dbs:
       return True
    else:
       return False

def disk_over_threshold(max_percent_disk_usage=80):
    """
    Check disk usage of postgresql data directory are over threshold
    given by parameter. This check will query the database to get
    the data directory. Then get from 'du -f' command the value to compare.
    return True if everything is ok
    return False if are over threshold or there was an error
    """
    status, result_list = pg.query('SELECT setting \
                                    FROM pg_settings \
                                    WHERE name = \'data_directory\' ;')
    if status:
       data_dir = str(result_list[0][0])
       try:
          bytes_usage = int(subprocess.check_output(['du','-s', data_dir],stderr=subprocess.STDOUT).split()[0])
       except Exception as e:
          print "Error getting postgresql disk usage: {} ".format(e)
          bytes_usage = 0
       st = os.statvfs(data_dir)
       bytes_total = st.f_blocks * st.f_frsize
       percent_usage = bytes_usage * 100.0 / bytes_total
       if percent_usage > max_percent_disk_usage:
          return True
    return False

def conns_over_threshold(max_percent_conns=80):
    """
    Check if established database connections are over percent threshold
    given by parameter. This check will create a connection. If postgres
    is full of conns this check will fail.
    return True if everything is ok
    return False if connections are over threshold or there was an error
    """
    # get established connections and check results
    status,result_list = pg.query('SELECT sum(numbackends) \
                                   FROM pg_stat_database ;')
    if status:
       number_conns = int(result_list[0][0])
    else:
       return False
    # get max connections and check results
    status,result_list = pg.query('SELECT setting \
                                   FROM pg_settings \
                                   WHERE  name = \'max_connections\';')
    if status:
       max_conns = int(result_list[0][0])
    else:
       return False
    # check threshold of percentage
    percent_conns = number_conns * 100.0 / max_conns
    if percent_conns > max_percent_conns:
       return True
    else:
       return False

if __name__ == "__main__":
    PROGRAM_NAME = str(__file__)
    parser = optparse.OptionParser("usage: " + PROGRAM_NAME +
                                   " --min-databases 1"
                                   " --max-percent-disk-usage 80"
                                   " --max-percent-connections 80".format())
    parser.add_option("-d", "--min-databases", \
                      dest="min_dbs", \
                      type="int", \
                      default="1", \
                      help="minimum number of databases threshold")
    parser.add_option("-u", "--max-percent-disk-usage", \
                      dest="max_percent_disk_usage", \
                      type="float", \
                      default=80, \
                      help="maximum percent disk usage across whole disk")
    parser.add_option("-c", "--max-percent-connections", \
                      dest="max_percent_conns", \
                      type="float", \
                      default=80, \
                      help="maximum percent established connections")

    (options, args) = parser.parse_args()
    error = False

    if dbs_under_threshold(min_dbs=options.min_dbs):
       error = True
       print ('Number of databases are under threshold {} '
             ''.format(options.min_dbs))

    if disk_over_threshold(max_percent_disk_usage=options.max_percent_disk_usage):
       error = True
       print ('Disk usage of postgresql is over {}% of the total disk '
             ''.format(options.max_percent_disk_usage))

    if conns_over_threshold(max_percent_conns=options.max_percent_conns):
       error = True
       print ('Number of established connections is over {}% of max connections'
             ''.format(options.max_percent_conns))

    if not error:
       print "Everything is under control"
       sys.exit(0)
    else:
       sys.exit(1)
