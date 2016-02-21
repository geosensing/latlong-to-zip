#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reverse Geocoding 

"""

import sys
import csv
import json
import sqlite3
import logging
import time
import optparse
from urllib import urlopen
from ConfigParser import ConfigParser
#from lxml import etree

COMMIT_INTERVAL = 10


def setup_logger():
    """ Set up logging
    """
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='latlong2zip.log',
                        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def parse_command_line(argv):
    """Command line options parser for the script
    """
    usage = "usage: %prog [options] <input file>"

    parser = optparse.OptionParser(add_help_option=False, usage=usage)
    parser.add_option("-i", "--import", action="store_true",
                      dest="importfile",
                      help="Import lat/long to database")
    parser.add_option("-a", "--askgeo", action="store_true",
                      dest="askgeo",
                      help="Request AskGeo for Zip code")
    parser.add_option("-o", "--output", action="store",
                      dest="output",
                      help="Output file with Zip code")
    parser.add_option("-?", "--help", action="help")

    return parser.parse_args(argv)


def import_file(options):
    """Import new lat/long to database
    """

    dbconn = sqlite3.connect(options.db)
    dbcur = dbconn.cursor()
    dbcur.execute('''create table if not exists UsZcta2010 (
        id   INTEGER    PRIMARY KEY AUTOINCREMENT,
        lat  REAL,
        long REAL,
        zip  CHAR( 6 ),
        json_id INTEGER,
        UNIQUE ( lat, long ))''')

    dbcur = dbconn.cursor()

    # Query row count before import
    dbcur.execute('''select count(id) from UsZcta2010''')
    r = dbcur.fetchone()
    before = r[0]
    logging.info("Rows count before import: {0:d}".format((before)))

    f = open(options.input)
    reader = csv.DictReader(f)
    i = 0
    loc = set()
    for r in reader:
        if i % 1000 == 0:
            logging.info("Importing...{0:d}".format(i))
        i += 1
        loc.add((r['latitude'], r['longitude']))
        dbcur.execute('''insert or ignore into UsZcta2010 (lat, long) values
                         (?, ?)''', (r['latitude'], r['longitude']))
    logging.info("Import finished (total: {0:d}, unique: {1:d})".format(i, len(loc)))
    f.close()

    dbconn.commit()

    # Query row count after import
    dbcur.execute('''select count(id) from UsZcta2010''')
    r = dbcur.fetchone()
    after = r[0]
    logging.info("Rows count after import: {0:d}".format((after)))
    logging.info("Imported {0:d} new lat/long".format((after - before)))
    dbconn.close()


def askgeo2zip(options):
    """Request ZIP code from AskGeo for new lat/long in database
    """

    batchsize = options.batch
    dbconn = sqlite3.connect(options.db)
    dbcur = dbconn.cursor()

    dbconn2 = sqlite3.connect(options.json_db)
    dbcur2 = dbconn2.cursor()
    dbcur2.execute('''create table if not exists json (
        id   INTEGER    PRIMARY KEY AUTOINCREMENT,
        points TEXT,
        json TEXT)''')

    terminate = False
    commit_count = 0
    while not terminate:
        dbcur.execute("select id, lat, long from UsZcta2010 where lat <> '' "
                      "and zip is null order by id limit ?", (batchsize,))
        rows = dbcur.fetchall()
        count = len(rows)
        if count == 0:
            logging.info('Completed!!!')
            break
        logging.info("ID: {0:d}".format((rows[0][0])))
        points_list = ','.join(['({0!s},{1!s})'.format(r[1], r[2]) for r in rows])
        points = '%3B'.join(['{0!s}%2C{1!s}'.format(r[1], r[2]) for r in rows])
        error = 0
        while True:
            try:
                json_str = urlopen("http://api.askgeo.com/v1/%s/%s/query.json?"
                                   "points=%s&databases=UsZcta2010" %
                                   (options.account, options.api_key,
                                    points)).read()
                j = json.loads(json_str)
                if j['code'] != 0:
                    error += 1
                    logging.warn("AskGeo return error code ({0:d}): {1:d}, {2!s}".format(error, j['code'], j['message']))
                    if error > options.max_errors:
                        logging.error("Maximum (%d) AskGeo return error "
                                      "code!!!" % (error))
                        terminate = True
                        break
                    logging.warn("Sleep for {0:d} seconds".format((error * error * 5)))
                    time.sleep(error * error * 5)
                    continue
            except Exception as e:
                error += 1
                logging.warn("AskGeo request error ({0:d}): {1!s}".format(error, e))
                if error > options.max_errors:
                    logging.error('Maximum ({0:d}) AskGeo request error!!!'.format(
                                  (error)))
                    terminate = True
                    break
                logging.warn("Sleep for {0:d} seconds".format((error * error * 5)))
                time.sleep(error * error * 5)
                continue
            dbcur2.execute('''insert or ignore into json (points, json) values
                              (?, ?)''', (points_list, json_str))
            json_id = dbcur2.lastrowid
            for i in xrange(count):
                r = rows[i]
                try:
                    zipcode = j['data'][i]['UsZcta2010']['ZctaCode']
                except Exception as e:
                    zipcode = ''
                    logging.warn("Cannot get zip code for lat/long: ({0:f}, {1:f})".format(r[1], r[2]))
                    pass
                dbcur.execute('''update UsZcta2010 set zip=?, json_id=? where
                                 id = ?''', (zipcode, json_id, r[0]))
            commit_count += 1
            if commit_count % COMMIT_INTERVAL == 0:
                dbconn.commit()
                dbconn2.commit()
            break
    # Last commit before close if requires
    if commit_count % COMMIT_INTERVAL != 0:
        dbconn.commit()
        dbconn2.commit()
    dbconn.close()
    dbconn2.close()


def addzipcode(options):
    """Add Zip code columns to file
    """

    dbconn = sqlite3.connect(options.db)
    dbcur = dbconn.cursor()
    f = open(options.input)
    o = open(options.output, 'wb')
    reader = csv.DictReader(f)
    header = reader.fieldnames
    if 'zipcode' not in header:
        header.append('zipcode')
    writer = csv.DictWriter(o, fieldnames=header)
    writer.writeheader()
    i = 0
    for r in reader:
        if i % 1000 == 0:
            logging.info("Exporting...({0:d})".format(i))
        zipcode = ''
        if r['latitude'] != '':
            dbcur.execute('''select zip from UsZcta2010 where lat = ? and
                             long = ?''', (r['latitude'], r['longitude']))
            res = dbcur.fetchone()
            if res[0] is None or res[0] == '':
                logging.warn("No ZIP code for {0!s}, {1!s}".format(r['latitude'],
                             r['longitude']))
            else:
                zipcode = res[0]
        r['zipcode'] = zipcode
        writer.writerow(r)
        i += 1
    logging.info("Export finished ({0:d})".format(i))
    f.close()
    o.close()
    dbconn.close()

if __name__ == "__main__":
    options, args = parse_command_line(sys.argv)
    setup_logger()
    logging.info("latlong2zip.py (r1 2013/12/28)")
    config = ConfigParser()
    try:
        config.read('latlong2zip.cfg')
        options.db = config.get('askgeo', 'db')
        options.json_db = config.get('askgeo', 'json_db')
        options.account = config.get('askgeo', 'account')
        options.api_key = config.get('askgeo', 'api_key')
        options.batch = config.getint('askgeo', 'batch')
        options.max_errors = config.getint('askgeo', 'max_errors')
    except:
        logging.error("Configuration file not found or invalid")
        sys.exit(-1)

    if len(args) > 1:
        options.input = args[1]
    else:
        options.input = None

    if options.importfile:
        if options.input is None:
            logging.error("-i/--import requires input file")
            sys.exit(-1)
        logging.info("Import lat/long to database")
        import_file(options)
    if options.askgeo:
        logging.info("Query ZIP code from AskGeo for new lat/long in database")
        askgeo2zip(options)
    if options.output:
        if options.input is None:
            logging.error("-o/--output requires input file")
            sys.exit(-1)
        logging.info("Export Zip code to input file")
        addzipcode(options)