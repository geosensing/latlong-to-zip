Convert Lat/Long to ZIP code by Google Maps (Reverse) Geocoding API
================================================================================

REQUIREMENTS
============
- Python 2.7.5
- pygeocoder (https://pypi.python.org/pypi/pygeocoder)

INPUT FILES AND RESTRICTIONS
============================
Input CSV file must be contains 3 minimum columns :- 'uniqid', 'lat', and 'long'

INSTRUCTION
===========

Available command line options:-

latlong2zip.py r1 (2013/08/28)

Usage: latlong2zip.py [options] <input file>

Options:
  -h, --help            show this help message and exit
  -r, --refresh         Refresh query and update Lat/Lon by Google Maps
                        Geocoding API
  -o OUTFILE, --outfile=OUTFILE
                        CSV Output file name (default: output.csv)
                                                
FOR EXAMPLES :-
 # ./latlong2zip.py input.csv

The 'output.csv' will be created, with an additional column 'zipcode' 
filled by ZIP code belong to each 'lat' and 'long' columns 

LIMITATIONS
===========
The script will be terminated with "ERROR: Google Geocoding API usage over limit" due to
Google Maps (Reverse) Geocoding APIs usage limit about 2,500 query/IP/day

Ref: https://developers.google.com/maps/documentation/geocoding/#Limits

