import pymongo
import pylast
import time
import sys
from datetime import datetime

class Track:
	def __init__(self, playedTrack=None):
		#self.name = playedTrack.track.name
		#self.artist = playedTrack.track.artist
		self.timestamp = playedTrack.timestamp
		#self.album = playedTrack.track.get_album() 
		#self.date = playedTrack.playback_date

	def get_timestamp(self):
		return self.timestamp
	#pass

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

	print API_KEY
	print API_SECRET
	print temp_pass

	# Next function only works 'properly' (returning Unix time) on Unix machines
	# Sorry, Windows
	current = time.time()

	# Retrieve last 200 tracks
	tracks = user.get_recent_tracks(3)

	# Connect to local MongoDB instance
	client = pymongo.MongoClient()
	db = client.music

	for track in tracks:
		trackClass = Track(track)
		print trackClass.timestamp
		#print track

	sys.exit()

	result = db.tracks.insert_many(tracks)
	print result.inserted_ids

	#for track in tracks:
		# two options to retrieve time
		# we'll use the timestamp method, but strptime() method works
	#	date = time.strptime(tracks[-1].playback_date, "%d %o %Y, %H:%M")
	#	last_time = float(tracks[-1].timestamp)

		# retrieve the last time from Mongo
		# tracks.find.sort("_id", pymongo.DESCENDING).limit(1);

		# put all of these tracks into MongoDB

	#	print last_time
	#	print goal
	#	print n
	#	print date.tm_mon
	#	print date.tm_mday

		# We haven't gone far enough back
		#if(last_time > goal):
		#	last_n = n
		#	n *= 2
		# We've gone far enough back
		#else:
			# need to go through tracks to find last one before goal
		#	while last_n != n:
		#		if tracks[last_n].timestamp > goal:
		#			last_n += 1
		#		else:
		#			break
		
	#print last_n

if __name__ == "__main__":
	main()