![alt text](https://github.com/Roadeo/qbittorrent-peers-location-grafana/blob/main/worldmap.PNG)

<h2>A python script (along with instructions) to display the locations of all the peers your qBittorrent client is connected to in a Grafana worldmap dashboard.</h2>

Disclaimer : The steps I took to get this working might not be the most efficient. But this is all I could create with what I know at the moment. Feel free to (actually this is a request) to make changes and improve this. Thanks!

<h3>Pre-requisites</h3>

* python
	* pygeohash module (to convert latitude and longitude to geohash)
	* mariadb module (a quick google search for 'python mariadb' should tell you all you need to know about using this module)

* MariaDB (this should work with other similar databases but I haven't tried any of them yet)

* qBittorrent

* Grafana

<h3>Steps</h3>

* First step is to create the database which will contain the information about the IP addresses and their corresponding locations. I used this "https://lite.ip2location.com/database/db5-ip-country-region-city-latitude-longitude" since it is free and it had the latitude and longitude information which is enough precision to pipoint a peer on the map. Download the IPV4 CSV file from this link and follow the instructions given below in the same page to create a database and import the location data to a table.

![alt text](https://github.com/Roadeo/qbittorrent-peers-location-grafana/blob/main/ip2locationdb.PNG)

![alt text](https://github.com/Roadeo/qbittorrent-peers-location-grafana/blob/main/peer_list.PNG)

* Next, create a new table which I'll call peer_list to store the IP addresses along with their geohashes of all the peers which are connected at a given point in time. To create this table, which is in the same database as the ip2location table, I used:

CREATE TABLE peer_list (time int(11), ip_address varchar(15), geohash varchar(20));

Remember to grant the neccessary permissions on both the tables to your MariaDB user.	

* Now download the python script in this repository and fill in your credentials.
	* qBittorrent web API credentials
	* MariaDB credentials

Once you're done with this step, run the script once. If all goes well, you should be able to see the peer_list table populated with IP addresses and geohashes.

If you haven't already done so, install the Grafana world map plugin. You can find it here "https://grafana.com/grafana/plugins/grafana-worldmap-panel/".

![alt text](https://github.com/Roadeo/qbittorrent-peers-location-grafana/blob/main/query.PNG)

![alt text](https://github.com/Roadeo/qbittorrent-peers-location-grafana/blob/main/worldmap_settings_1.PNG)

![alt text](https://github.com/Roadeo/qbittorrent-peers-location-grafana/blob/main/worldmap_settings_2.PNG)

* Once that's done, create a new panel in Grafana and change visualization option to worldmap panel. Change the database source to your MariaDB database. Choose the table name as peer_list, and the metric column as geohash. In the next row, change the Column:value to Column:geohash by right clicking it and typing in geohash. Then, at the end of the query options, change the format as option to table. Then we'll change the worldmap panel options in the right side. Change the values for min and max circle size to 1 since we're displaying each peer as a single dot and not as a bigger circle. Change location data to geohash. Finally, under field mapping, enter geohash in the geo_point/geohash field box.

And, if everything went correctly (or exactly like I did lol), you should start seeing a few dots appear on the map. You can change the color of the dots by changing the color for the thresholds in previous step.

* Now, all that's left is to add a cron entry to execute the script at regular intervals and we're done. :)
