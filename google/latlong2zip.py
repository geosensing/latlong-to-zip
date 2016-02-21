#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import signal
import optparse
import csv

from pygeocoder import Geocoder, GeocoderError

"""Script default configuration
"""
LOGFILE = 'latlong2zip.log'

class Logger(object):
    """Standard output wrapper class
    """
    def __init__(self, filename=None):
        self.terminal = sys.stdout
        if filename == None:
            filename = os.path.splitext(__file__)[0] + '.log'
        self.log = open(filename, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

def LatLonToZip(lat, lon):
    """Returns Zip code for Lat/Lon (Using Google Maps Reverse Geocoding API)
       Usage Limit:
       https://developers.google.com/maps/documentation/geocoding/#Limits
    """
    try:
        results = Geocoder.reverse_geocode(lat, lon)
        return results[0].postal_code
    except Exception as e:
        print e.status
        if e.status != GeocoderError.G_GEO_ZERO_RESULTS:
            # Raise except if OVER_USAGE_LIMIT
            raise
        return None

def parse_command_line(argv):
    """Command line options parser for the script
    """
    usage = "usage: %prog [options] <input file>"
            
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-r", "--refresh", action="store_true", 
                      dest="refresh", default=False,
                      help="Refresh query and update Lat/Lon by Google Maps Geocoding API")    
    parser.add_option("-o", "--outfile", action="store", 
                      dest="outfile", default='output.csv',
                      help="CSV Output file name (default: output.csv)")
        
    return parser.parse_args(argv)

def main(options, args):
    with open(args[1], 'rb') as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        # Check input file contains minimum columns
        for c in ['uniqid', 'lat', 'long']:
            if c not in fields:
                print("ERROR: Input file don't have column '{0!s}'".format(c))
                return
        if 'zipcode' not in fields:
            fields.append('zipcode')

        if os.path.exists(options.outfile) and not options.refresh:
            with open(options.outfile) as of:
                count = len(list(of)) - 1
                for i in range(0, count):
                    reader.next()
            of = open(options.outfile, 'ab')
            writer = csv.DictWriter(of, fieldnames=fields)
            if count < 0:
                writer.writeheader()
        else:
            of = open(options.outfile, 'wb')
            writer = csv.DictWriter(of, fieldnames=fields)
            writer.writeheader()
        for r in reader:
            lat = float(r['lat']) 
            lon = float(r['long'])
            try:
                print("Query zipcode for lat = {0:f}, long = {1:f}".format(lat, lon))
                zipcode = LatLonToZip(lat, lon)
                if zipcode == None:
                    zipcode = 'N/A'
                r['zipcode'] = zipcode
                writer.writerow(r)
            except:
                writer.writerow(r)
                print("ERROR: Google Geocoding API usage over limit")
                break
        of.close()
                
def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    os._exit(1)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    sys.stdout = Logger(LOGFILE)
    signal.signal(signal.SIGINT, signal_handler)
    print("{0!s} r1 (2013/08/28)\n".format((os.path.basename(sys.argv[0]))))
    (options, args) = parse_command_line(sys.argv)
    if len(args) < 2:
        print("Please specific input file (CSV)")
        sys.exit(-1)
    main(options, args)
