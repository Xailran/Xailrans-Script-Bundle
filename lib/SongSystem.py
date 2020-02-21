import codecs
import os
#---------------------------------------
#   Next Song Functions
#---------------------------------------
def SongReport(Parent, MySet, numsongs):
	if numsongs > MySet.NSmaxsongs:
		message = MySet.NStoomany.format(str(MySet.NSmaxsongs), str(numsongs))
		numsongs = MySet.NSmaxsongs
		Parent.SendStreamMessage(message)
	songs = Parent.GetSongQueue(numsongs)
	songlist = []
	for obj in songs:
		songlist.append(obj.Title)
	if len(songlist) != numsongs:
		songs = Parent.GetSongPlaylist(numsongs - len(songlist))
		for obj in songs:
			songlist.append(obj.Title)
	message = ""
	if not songlist:
		message = MySet.NSempty
	elif len(songlist) == 1:
		message = MySet.NSsingle.format(songlist[0])
	else:
		message = MySet.NSmultiple.format(", ".join(songlist))
	return message

def PlaylistProcess(Parent, MySet):
	number = 100
	songs = Parent.GetSongPlaylist(number)
	while len(songs) == number:
		number += 100
		songs = Parent.GetSongPlaylist(number)
	Parent.SendStreamMessage("Songlist length set at " + str(len(songs)) + " songs.")
	File = os.path.join(os.path.dirname(__file__), "../" + MySet.playlistname + ".txt")
	if os.path.exists(File):
		Parent.SendStreamMessage("The file {0}.txt is already taken! Please set another file in the UI".format(MySet.playlistname))
		return
	for obj in songs:
		textline = obj.URL
		with codecs.open(File, "a", "utf-8") as f:
			f.write(u"" + textline + "\r\n")
	Parent.SendStreamMessage("Playlist has been exported!")