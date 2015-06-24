### Get Zip codes for Lat/Long Using Google Maps Reverse Geocoding API

The script uses the [Google Maps API](https://developers.google.com/maps/) to reverse geocode latitude and longitude to zip code. The script takes a csv with at least the following 3 columns: 'uniqid', 'lat', and 'long' (See [sample input file](input.csv).) And produces a csv with zip codes appended to the existing columns.  

Note that the Google Maps Reverse Geocoding API [usage limit](https://developers.google.com/maps/documentation/geocoding/#Limits) is 2,500 queries/IP/day. 

#### Running the Script

##### Requirements
- Python 2.7.5
- [pygeocoder](https://pypi.python.org/pypi/pygeocoder)

##### Usage: 

`latlong2zip.py [options] input_file`

##### Command line options:
```
Options:
  -h, --help            show this help message and exit
  -r, --refresh         Refresh query and update Lat/Lon by Google Maps
                        Geocoding API
  -o OUTFILE, --outfile=OUTFILE
                        CSV Output file name (default: output.csv)
```

##### Example:
`python latlong2zip.py input.csv`

The script will produce output.csv with appends a 'zipcode' column to input.csv.

**Note** The script will terminate with "ERROR: Google Geocoding API usage over limit" if [Google Maps (Reverse) Geocoding APIs usage limit](https://developers.google.com/maps/documentation/geocoding/#Limits) of 2,500 queries/IP/day is exceeded.