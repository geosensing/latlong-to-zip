### Convert Large number of Lat/Longs to zip codes using AskGeo

The script is tailored for large batch jobs. It uses the [AskGeo API](https://askgeo.com/) to reverse geocode latitude and longitudes. It takes a csv.

#### Application
The script was used to produce zip codes for [Database on Ideology, Money in Politics, and Elections](http://data.stanford.edu/dime). Database with zip codes is posted on Harvard DVN ([see here](http://dx.doi.org/10.7910/DVN/28957)).

#### Details About the Script

The script creates 2 databases:

1. Main database file: askgeo.db contains table "UsZcta2010"
<pre>
UsZcta2010 (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        lat     REAL,
        long    REAL,
        zip     CHAR( 6 ),
        json_id INTEGER,
        UNIQUE ( lat, long )
        )
</pre>

2. UsZcta2010.db contains table "json" use for store all JSON reply by AskGeo for each request.
<pre>
json (
        id   INTEGER    PRIMARY KEY AUTOINCREMENT,
        points TEXT,
        json TEXT)   
</pre>

NOTE THAT: This database quite large (12GB for 2.8 millions request)

#### Usage

<pre><code>Usage: latlong2zip.py [options] input_file </code></pre>

Command line options for the scriptshown below:
<pre><code>
Options:
  -i, --import          Import lat/long to database
  -a, --askgeo          Request AskGeo for Zip code
  -o OUTPUT, --output=OUTPUT
                        Output file with Zip code
  -?, --help
</code></pre>

#### Example

1. Import new lat/long to database
<pre><code>    python latlong2csv.py -i contribDB_1980.csv</code></pre>

2. Query ZIP code from AskGeo for new lat/long in database
<pre><code>     python latlong2csv.py -a</code></pre>

3. Export (append) ZIP code to input file and save to output file
<pre><code>python latlong2csv.py -o contribDB_1980_zipcode.csv contribDB_1980.csv</code></pre>
