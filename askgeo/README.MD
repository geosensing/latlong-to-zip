### Convert Large number of Lat/Longs to ZIP code using AskGeo API

####DATABASES & TABLES

The script creates 2 databases:-

1) Main database file: askgeo.db contains table "UsZcta2010"

UsZcta2010 (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        lat     REAL,
        long    REAL,
        zip     CHAR( 6 ),
        json_id INTEGER,
        UNIQUE ( lat, long )
        )

2) UsZcta2010.db contains table "json" use for store all JSON reply by AskGeo for each request.

json (
        id   INTEGER    PRIMARY KEY AUTOINCREMENT,
        points TEXT,
        json TEXT)   

NOTE THAT: This database quite large (12GB for 2.8 millions request)

####How to Run

The script command line options shown below :-

<pre><code>
Usage: latlong2zip.py [options] <input file>

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

    python latlong2csv.py -o contribDB_1980_zipcode.csv contribDB_1980.csv
