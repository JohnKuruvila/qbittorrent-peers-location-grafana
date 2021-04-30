import requests
import json
import socket, struct
import mariadb 
import time
import pygeohash

#To convert the IP address in xxx.xxx.xxx.xxx to a decimal number
def ip2long(ip):
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]

#qbittorrent credentials
server_ip = ""
qbport = ""
qbusername = ""
qbpassword = ""

server_address = "http://" + server_ip + ":" + qbport

s = requests.Session()
s.get(server_address + "/api/v2/auth/login?username=" + qbusername + "&password=" + qbpassword)
torrents = json.loads(s.get(server_address + "/api/v2/torrents/info").text)

#Logging into mariadb server / Enter your mariadb credentials here
mydb = mariadb.connect(
          host="",
          port=,
          user="",
          password="",
          database="",
          autocommit=True
)

current_time = str(int(time.time())) 

for torrent in torrents:
    torrent_peers = json.loads(s.get(server_address + "/api/v2/sync/torrentPeers?hash=" + torrent["hash"]).text)

    #Get IP address of every peer of every torrent
    for peer in torrent_peers["peers"]:
        ip = peer.split(":")[0]
        long_ip = ip2long(ip)

        mycursor = mydb.cursor()

        query="SELECT latitude,longitude FROM ip2location.ip2location_db5 WHERE " + str(long_ip) + " BETWEEN ip_from AND ip_to;"
        mycursor.execute(query)
        results = mycursor.fetchall()[0]
        latitude = results[0]
        longitude = results[1]

        geohash = pygeohash.encode(latitude, longitude)

        query = "INSERT INTO ip2location.peer_list(time, ip_address, geohash) VALUES (" + current_time + ",'" + str(ip) + "','" + geohash + "');"
        mycursor.execute(query)


s.get(server_address + "/api/v2/auth/logout")

