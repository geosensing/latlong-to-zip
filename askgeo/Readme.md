### Convert Large number of Lat/Longs to zip codes using AskGeo

The script uses the [AskGeo API](https://askgeo.com/) to reverse geocode latitude and longitudes. It is customized for large batch jobs. For instance, the script was used to produce zip codes for [Database on Ideology, Money in Politics, and Elections](http://data.stanford.edu/dime). Database with zip codes is posted on Harvard DVN ([see here](http://dx.doi.org/10.7910/DVN/28957)).

AskGeo also returns zip code level information from the 2010 US Census. These data are stored in [uszcta2010.csv](uszcta2010.csv).

#### Details About the Script

The script creates 2 databases:

1. Main database file: askgeo.db contains table "UsZcta2010"
```
UsZcta2010 (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        lat     REAL,
        long    REAL,
        zip     CHAR( 6 ),
        json_id INTEGER,
        UNIQUE ( lat, long )
        )
```

2. UsZcta2010.db contains table "json" to store all JSON returned by AskGeo for each request. 
```
json (
        id   INTEGER    PRIMARY KEY AUTOINCREMENT,
        points TEXT,
        json TEXT)   
```

#### Usage

Get started by getting the API Key from GeoNames. Next, add the account information and api_key in the [latlong2zip.cfg](latlong2zip.cfg) file. To run the script:

`latlong2zip.py [options] input_file`

**Command line options**

```
Options:
  -i, --import          Import lat/long to database
  -a, --askgeo          Request AskGeo for Zip code
  -o OUTPUT, --output=OUTPUT
                        Output file with Zip code
  -?, --help
```

**Examples**

1. Import new lat/long to database
`python latlong2csv.py -i contribDB_1980.csv`

2. Query ZIP code from AskGeo for new lat/long in database
`python latlong2csv.py -a`

3. Export (append) ZIP code to input file and save to output file
`python latlong2csv.py -o contribDB_1980_zipcode.csv contribDB_1980.csv`
