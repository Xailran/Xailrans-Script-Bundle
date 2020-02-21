#---------------------------------------
#   Encoded Song Functions
#---------------------------------------
ESphrase = "XSB%%SIP"
old_songs = []
request_data = ("","")

def EncodingReport(Parent, MySet):
	"""Detects if a song was skipped"""
	song = Parent.GetNowPlaying()
	if request_data[0] == "Empty song list" and request_data[1] == "Empty song list":
		return ListSongs(Parent)
	#If current song was not the already playing song, or the one that was supposed to play next
	songlist = [x.replace(ESphrase, "") for x in old_songs]
	if song.Key not in songlist:
		#For songs in the backup playlist
		songcost = SongPermission(Parent, MySet)
		if old_songs[1].startswith(ESphrase):
			message = MySet.SEplaylistmessage.format(old_songs[1].replace(ESphrase, ""), request_data[1], Parent.GetCurrencyName())
		#For song requests
		else:
			songcost = SongPermission(Parent, MySet)
			message = MySet.SEmessage.format(old_songs[1], request_data[1], songcost, Parent.GetCurrencyName())
			Parent.AddPoints(request_data[0], request_data[1], songcost)
		Parent.SendStreamMessage(message)
	return ListSongs(Parent)

def SongPermission(Parent, MySet):
	"""Finds cost for user to request a song"""
	if Parent.HasPermission(request_data[0], "Moderator", ""):
		if not MySet.casterRefund:
			if Parent.HasPermission(request_data[0], "Caster", ""):
				return 0
		return MySet.modsongcost
	if Parent.HasPermission(request_data[0], "Subscriber", ""):
		return MySet.subsongcost
	if Parent.HasPermission(request_data[0], "Regular", ""):
		return MySet.regularsongcost
	return MySet.viewersongcost

def ListSongs(Parent):
	"""Gets upcoming songs"""
	# Gets current song
	global old_songs
	songlist = []
	song = Parent.GetNowPlaying()
	songlist.append(song.Key)
	numsongs = 1
	# Gets next song
	songs = Parent.GetSongQueue(numsongs)
	for obj in songs:
		songlist.append(obj.Title)
	# Sets song as belonging to playlist if not enough in queue
	if len(songlist) != numsongs + 1:
		songs = Parent.GetSongPlaylist(numsongs + 1 - len(songlist))
		for obj in songs:
			songlist.append(ESphrase + obj.Title)
	old_songs = songlist

def NextSong(Parent):
	"""Gets data of user who requested next song"""
	global request_data
	songs = Parent.GetSongQueue(1)
	next_song = ""
	for obj in songs:
		next_song = obj.Title
	if not next_song:
		songs = Parent.GetSongPlaylist(1)
		for obj in songs:
			next_song = obj.Title
	if not next_song:
		return "Empty song list", "Empty song list"
	requestedID = songs[0].RequestedBy
	requestedName = songs[0].RequestedByName
	request_data = (requestedID, requestedName)