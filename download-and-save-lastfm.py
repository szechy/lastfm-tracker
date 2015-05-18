import pymongo
import pylast
import sys
import re
import time

class Track:
	def __init__(self, playedTrack=None):
		# A Jack U song broke my previous ASCII strings implementation :(
		# so straight to Unicode
		self.track		= unicode(playedTrack.track.title)
		self.artist 	= unicode(playedTrack.track.artist)
		self.timestamp 	= str(playedTrack.timestamp)
		self.album 		= str(playedTrack.album)

		# regex to parse the playback_date into useful data
		matchObj 		= re.match("^(\d{1,2})\s(\w{3,4})\s(\d{4})," +
			"\s(\d{1,2}):(\d{1,2})$", playedTrack.playback_date)
		self.day 		= int(matchObj.group(1))
		self.month 		= str(matchObj.group(2))
		self.year 		= int(matchObj.group(3))
		self.hour		= int(matchObj.group(4))
		self.minute 	= int(matchObj.group(5))

		# Create a dictionary out of the data we just created
		# which is what pymongo's insert function accepts as input
		self.document 	= self.toDict()

	def toDict(self):
		dict = {"track" : self.track, 			"artist" : self.artist, 
				"timestamp": self.timestamp, 	"day" : self.day, 
				"month" : self.month, 			"year" : self.year,
				"hour" : self.hour, 			"minute" : self.minute}
		return dict

def main():
	# Unique application values
	keys = open('lastfm-info', 'r')
	# Masking API keys in a local file, sorry everyone
	TEMP_API_KEY = keys.readline();
	API_KEY = TEMP_API_KEY.replace("\n", "")

	TEMP_API_SECRET = keys.readline()
	API_SECRET = TEMP_API_SECRET.replace("\n", "")

	# To perform a write operation, need to auth myself
	username = "kenavt"
	# I think the fact I have to provide my password for auth is ridiculous
	# to access data for a public profile...
	temp_pass = keys.readline()
	password = pylast.md5(temp_pass.replace("\n", ""))

	network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)
	user = network.get_user(username)
	# Enable caching - important for going past 200 songs
	network.enable_caching()

	# Retrieve last 200 tracks - or whatever strikes your fancy.
	# Last.fm's API implements 200 track limit
	tracks = user.get_recent_tracks(20)
	index = 0
	songs = []
	for track in tracks:
		# import into custom Track class
		songs.append(Track(track))
		# debugging statements commented out below
		# uncommenting this gives the data pulled from Last.fm
		#print index
		#print songs[-1].track
		#print songs[-1].timestamp
		index += 1

	songs.reverse()
	index = 0

	# Connect to local MongoDB instance - replace with your own database
	client = pymongo.MongoClient()
	db = client.music

	# Retrieve highest timestamp entry from Mongo
	most_recent = db.tracks.find().sort("_id", pymongo.ASCENDING).limit(1)[0];
	# debugging statements commented out below:
	#print "Mongo says..."
	#print most_recent['timestamp']

	# loop through songs we've retrieved, until we catch up to latest Mongo
	for song in songs:
		most_recent_time = song.timestamp
		if most_recent_time > most_recent['timestamp']:
			# Boom: now insert into Mongo
			while index < len(songs):
				result = db.tracks.insert_one(songs[index].document)
				index += 1
			break
		index += 1

if __name__ == "__main__":
	main()