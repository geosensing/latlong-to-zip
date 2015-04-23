### Get zip codes for Lat/Longs Using Google Maps Reverse Geocoding API

Takes a csv file with at least the following 3 columns: 'uniqid', 'lat', and 'long'  and produces a csv with zip codes appended.

#### Running the Script

##### Requirements
- Python 2.7.5
- pygeocoder (https://pypi.python.org/pypi/pygeocoder)

##### Usage: 
<pre><code>latlong2zip.py [options] input_file</code></pre>

##### Command line options:
<pre><code>
Options:
  -h, --help            show this help message and exit
  -r, --refresh         Refresh query and update Lat/Lon by Google Maps
                        Geocoding API
  -o OUTFILE, --outfile=OUTFILE
                        CSV Output file name (default: output.csv)
</code></pre>

##### Example:
<pre> python latlong2zip.py input.csv</pre>

The script will produce 'output.csv' with appends a 'zipcode' column to columns in input.csv.

The script will terminate with "ERROR: Google Geocoding API usage over limit" if [Google Maps (Reverse) Geocoding APIs usage limit](https://developers.google.com/maps/documentation/geocoding/#Limits) of 2,500 query/IP/day is exceeded.
