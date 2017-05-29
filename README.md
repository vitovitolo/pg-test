# PG-TEST

## INSTALL 

Requirements: Debian 8 Jessie and python 2.7.9

This will install this Debian packages from official repo:
- postgresql-9.4
- python-psycopg2 2.5.4

The rest of the programs will be installed /opt/pg_scripts path


```
sudo apt-get install puppet 
sudo puppet apply --modulepath puppet/modules/ puppet/manifests/install.pp
```


## UNINSTALL

Be aware, this command will purge postgresql-9.4 from system including databases

```
sudo puppet apply --modulepath puppet/modules/ puppet/manifests/uninstall.pp
```

## CONFIG

The config file will be installed in /opt/pg_scripts/conf/config.py with some PostgreSQL info like: host, user, default db, etc

## USAGE

### Populate

This program creates 10 databases with 10 tables each and random rows in each table.
The names of the databases and tables are random

This program uses threads with no limits. Be carefull, you could collapse your postgresql database with high amount of connections.
```
python /opt/pg_scripts/bin/pg_populate.py --databases 10 --tables 10
```

#### Populat Thread Pool

This program is experimental and is written with ThreadPool.
You could configure the max connection that the program is allow to do against postgresql with MAX_CONNS constant in the code.

```
python /opt/pg_scripts/bin/pg_populate_pool.py --databases 10 --tables 10
```

### Perform some checks

This program checks some parameters:
- The number of databases are not under 10
- The percent of disk usage by postgresql across whole disk are not over 80%
- The percent of established connections to postgresql are not over 80% of the max connections

Returns exit status 0 when everything is ok

```
sudo python /opt/pg_scripts/bin/pg_checks.py --min-databases 10 --max-percent-disk-usage 80 --max-percent-connections 80
```

### Data info

This program get this info:
- Average size of the databases' data
- Percentile 90 of databases' data
- Total size across the entire database server

```
python /opt/pg_scripts/bin/pg_data_info.py
```

TODO
===
- Unit testing
- Handle exception properly
- Better error handling
- Create a func in pg_data_info to export the output to a metric system
- Finish pg_populate_pool.py program

