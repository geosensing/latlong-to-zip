### Latitude/Longitude to Zip Codes

Takes a csv with a list of latitudes and longitudes and finds the zip code in which they are in.

#### Background

**Some Reverse Geocoding Services**

* [Open Street Map](http://www.openstreetmap.org/) and [Nominatim](https://github.com/twain47/Nominatim)
* [AskGeo](http://askgeo.com/)
* [Google](https://developers.google.com/maps/)

**How do the data compare across different services?**

[DiffLatLong2ZipServicesCompared.xlxs](DiffLatLong2ZipServicesCompared.xlsx) compares lat/long to zip code mapping for 300 locations from [Google](https://developers.google.com/maps/), [AskGeo](http://askgeo.com/), and [OSM](http://www.openstreetmap.org/).

#### Scripts

* [AskGeo Script](askgeo) 
  * The script is tailored for large batch jobs. 
  * The script was used to produce zip codes for [Database on Ideology, Money in Politics, and Elections ](http://data.stanford.edu/dime). Database with zip codes is posted on [Harvard DVN](http://dx.doi.org/10.7910/DVN/28957). 

* [Google Script](google)
  * Google has a rate limitation of 2,500 query/IP/day. The pricing for more extensive packages is prohitibitive.

#### License
Scripts are released under the [MIT License](https://opensource.org/licenses/MIT).
