#!/usr/bin/python
# -*- coding: utf-8 -*-
#Parent = Parent # pylint: disable=invalid-name
"""Streamlabs Chatbot Script"""
#---------------------------------------
# Libraries and references
#---------------------------------------
import codecs
import json
import os
import sys
import ctypes
import winsound
import re
import threading
from time import time

#Script Bundle Libraries
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
import SongSystem
import EncodedSongs
import OnJoin
import WordCount

#---------------------------------------
# Script information
#---------------------------------------
ScriptName = "Xailran's Script Bundle"
Website = "https://www.xailran.com/"
Creator = "Xailran"
Version = "1.3.3"
Description = "Song request functionality, word counts, and other parameters"

#---------------------------------------
# Versions
#---------------------------------------
"""
1.3.3 - Improved user customization settings
1.3.2 - Song encoding will now identify if the song was in the playlist or requested, and will treat it accordingly
1.3.1 - Fixed issues with nextsong, and changed it to be a parameter, rather than a built in command
1.3.0 - Added exclusion list for word/message leaderboard. Added $number, $interrupt, $filelines, and $deleteline parameters!
1.2.1 - Bug fixes for next song and word count modules
1.2.0 - Added $delay parameter
1.1.1 - Fixed regex so more leaderboard could detect numbers higher than 9. Added $messagecount, $wordpos, and $messagepos to Word Count Parameters
1.1.0 - Added word count parameters, including leaderboard
1.0.0 - Initial Release!
"""

#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YES = 6
oldsonglist = []
requestedData = ("","")
wordcountparameters = ["$topwords", "$topmessages", "$wordcount", "$numbercount", "$emotecount", "$commandcount", "$messagecount", "$wordpos", "$messagepos"]
tickmessages = {}

#---------------------------------------
# Settings functions
#---------------------------------------
def SetDefaults():
	"""Set default settings function"""
	winsound.MessageBeep()
	returnValue = MessageBox(0, u"You are about to reset the settings, "
								"are you sure you want to continue?"
							 , u"Reset settings file?", 4)

	if returnValue == MB_YES:
		Settings(None, None).Save(settingsFile)
		MessageBox(0, u"Settings successfully restored to default values!"
					  "\r\nMake sure to reload script to load new values into UI"
				   , u"Reset complete!", 0)

def ReloadSettings(jsonData):
	"""Reload settings on Save"""
	global MySet
	MySet.Reload(jsonData)

#---------------------------------------
# UI functions
#---------------------------------------
def OpenReadMe():
	"""Open the readme.txt in the scripts folder"""
	location = os.path.join(os.path.dirname(__file__), "README.txt")
	os.startfile(location)

def OpenFolder():
	"""Open Store Script Folder"""
	location = (os.path.dirname(os.path.realpath(__file__)))
	os.startfile(location)

def ExportPlaylist():
	"""Save playlist, and then open it"""
	SongSystem.PlaylistProcess(Parent, MySet)
	location = os.path.join(os.path.dirname(__file__), MySet.playlistname + ".txt")
	os.startfile(location)

def wcpHelp():
	"""Opens an information box containing all the parameters available for Word Counts"""
	MessageBox(0, "\r\n $topwords(num) - Shows the top (num) users with the most words"
				"\r\n $wordpos - Shows the user/targets position on the above leaderboard"
				"\r\n $topmessages(num) - Shows the top (num) users with the most messages"
				"\r\n $messagepos - Shows the user/targets position on the above leaderboard"
				"\r\n $wordcount - Total words said, excluding commands, emotes, and numbers counted"
				"\r\n $emotecount - Total emotes used in chat (global or local channel emotes only)"
				"\r\n $numbercount - Total amount of numbers used in chat"
				"\r\n $commandcount - Total number of commands used in chat"
				"\r\n $messagecount - Total number of messages sent to chat", 0)

#---------------------------------------
# Optional functions
#---------------------------------------
def HasPermission(data, permission, permissioninfo):
    """Return true or false dending on if the user has permission.
    Also sends permission response if user doesn't"""
    if not Parent.HasPermission(data.User, permission, permissioninfo):
        message = MySet.notperm.format(data.UserName, permission, permissioninfo)
        Parent.SendStreamMessage(message)
        return False
    return True

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
	"""data on Load, required function"""
	global MySet
	MySet = Settings(Parent, settingsFile)
	global oldsonglist, requestedData
	EncodedSongs.ListSongs(Parent)
	EncodedSongs.NextSong(Parent)
	OnJoin.LoadJoinedUsers(Parent)
	if MySet.enableWCP:
		EL = threading.Thread(target=WordCount.EmoteList, args=(Parent))
		EL.daemon = True
		EL.start()
		LWC = threading.Thread(target=WordCount.LoadWordCounts, args=())
		LWC.daemon = True
		LWC.start()

def Execute(data):
	"""Required Execute data function"""
	#Next Songs Package
	if MySet.enableWCP and (data.IsChatMessage() or (MySet.countWhispers and data.IsWhisper())):
		WordCount.CollectWords(data, MySet)
	
	elif data.GetParam(0).lower() == MySet.PEcommand.lower():
		if not HasPermission(data, MySet.PEpermission, MySet.PEpermissioninfo):
			return
		SongSystem.PlaylistProcess(Parent, MySet)

def Tick():
	"""Required Tick function"""
	if not Parent.IsOnCooldown(ScriptName, "encoding"):
		Parent.AddCooldown(ScriptName, "encoding", 5)
		if MySet.SEenabled:
			EncodedSongs.EncodingReport(Parent, MySet)
			EncodedSongs.NextSong(Parent)

	if not Parent.IsOnCooldown(ScriptName, "OnJoin"):
		Parent.AddCooldown(ScriptName, "OnJoin", 5)
		if MySet.joinenabled:
			OnJoin.PointGiving(Parent, MySet)

	if tickmessages:
		currenttime = time()
		removallist = []
		for key, message in tickmessages.iteritems():
			if currenttime >= key:
				Parent.SendStreamMessage(message)
				removallist.append(key)
		for x in removallist:
			del tickmessages[x]

def Parse(parseString, userid, username, targetid, targetname, message):
	"""Adds parameters to be used in commands"""
	#Number parameter
	#Group 0 = full parameter, group 1 = min, group 2 = max. group 3 = number to be tested, group 4 = success message, group 5 = failure message
	if "$number" in parseString:
		np = re.search(r'\$number\("?(\d+)"?,\s*"?(\d+)"?,\s*"?(\d+)"?,\s*"([^"]*)",\s?"?([^"]*)"\)', parseString)
		if np:
			if int(np.group(1)) <= int(np.group(3)) < int(np.group(2)):
				parseString = parseString.replace(np.group(0), np.group(4))
			else:
				parseString = parseString.replace(np.group(0), np.group(5))

	#Word count parameters and replacement function
	if any([x in parseString for x in wordcountparameters]):
		parseString = WordCount.Parameters(parseString, userid, username, targetid, targetname, message, MySet)
	
	#Next Song parameter
	if "$songs" in parseString:
		ns = re.search(r'\$songs\((\d+)\)', parseString)
		if ns:
			message = SongSystem.SongReport(Parent, MySet, int(ns.group(1)))
		parseString = parseString.replace(ns.group(0), message)

	#Filelines parameter
	if "$filelines" in parseString:
		cl = re.search(r'\$filelines\(([^\)]*)\)', parseString)
		if cl:
			path = cl.group(1)
			Item = []
			if os.path.exists(path):
				with codecs.open(path, encoding="utf-8-sig", mode="r") as file:
					Item = [line.strip() for line in file]
			parseString = parseString.replace(cl.group(0), str(len(Item)))

	#DeleteLines parameter
	#group 0 = full match, group 1 = path, group 2 = line, group 3 = success message, group 4 = fail message
	if "$deleteline" in parseString:
		dl = re.search(r'\$deleteline\("([^"]*)",\s*(\d+),\s*"([^"]*)",\s*"([^"]*)"\)', parseString)
		if dl:
			path = dl.group(1)
			complete = False
			if os.path.exists(path):
				with codecs.open(path, encoding="utf-8-sig", mode="r") as file:
					Item = [line.strip() for line in file]
				filestr = ""
				for x in range(0, len(Item)):
					if x == int(dl.group(2)):
						complete = True
						continue
					if filestr != "":
						filestr += "\r\n"
					filestr += Item[x]
				with codecs.open(path, "w", "utf-8") as file:
					file.write(filestr)
			if complete:
				parseString = parseString.replace(dl.group(0), dl.group(3))
			else:
				parseString = parseString.replace(dl.group(0), dl.group(4))

	#Delay parameter
	if "$delay" in parseString:
		dp = re.search(r'\$delay\(\"?(\d+)\"?\,\s*(.*)\)', parseString)
		if dp:
			global tickmessages
			tickmessages[int(dp.group(1)) + int(time())] = dp.group(2)
			parseString = parseString.replace(dp.group(0), "")

	#If parameter

	#Interrupt parameter
	#group 1 = full parameter, group 2 = interrupted parameter
	if "$interrupt" in parseString:
		ip = re.search('\$interrupt\[([^\]]*)\]', parseString)
		if ip:
			parseString = parseString.replace(ip.group(0), ip.group(1))
	return parseString

def Unload():
	"""Optional function for when scripts are reloaded or chatbot is closed"""
	OnJoin.SaveJoinedUsers()
	WordCount.SaveWordCounts()

#---------------------------------------
# Classes
#---------------------------------------
class Settings:
	""" Loads settings from file if file is found if not uses default values"""

	# The 'default' variable names need to match UI_Config
	def __init__(self, parent, settingsFile=None):
		if settingsFile and os.path.isfile(settingsFile):
			with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
				self.__dict__ = json.load(f, encoding='utf-8-sig')
		else: #set variables if no custom settings file is found
			self.NStoomany = "Too many songs requested, reducing to {0}"
			self.NSmaxsongs = 10
			self.NSempty = "There are no songs in the queue"
			self.NSsingle = "The next song is: {0}"
			self.NSmultiple = "The next songs are: {0}"
			self.SEenabled = True
			self.SEmessage = "Uh-oh, {0} was skipped due to YouTube encoding issues! Refunding {1} {2} {3}"
			self.SEplaylistmessage = "Uh-oh, {0} was skipped due to YouTube encoding issues! (No refund, song was in back-up playlist)"
			self.viewersongcost = 500
			self.regularsongcost = 500
			self.subsongcost = 250
			self.modsongcost = 250
			self.casterRefund = True
			self.joinenabled = True
			self.joinpoints = 1000
			self.joinlogmessage = "{0} has joined the stream for the first time. They were given {1} {2}"
			self.PEcommand = "!export"
			self.playlistname = "playlist"
			self.PEpermission = "Caster"
			self.PEpermissioninfo = ""
			self.notperm = "{0} -> you don't have permission to use this command. permission is: [{1} / {2}]"
			self.enableWCP = True
			self.countWhispers = False
			self.countCommands = True
			self.countEmotes = True
			self.countNumbers = True
			self.countExclusionList = "Nightbot Moobot"

		self.parent = parent

	# Reload settings on save through UI
	def Reload(self, data):
		"""Reload settings on save through UI"""
		parent = self.parent
		self.__dict__ = json.loads(data, encoding='utf-8-sig')
		self.parent = parent
	
	def Save(self, settingsfile):
		""" Save settings contained within the .json and .js settings files. """
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
				json.dump(self.__dict__, f, encoding="utf-8", ensure_ascii=False)
			with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
				f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8', ensure_ascii=False)))
		except ValueError:
			MessageBox(0, u"Settings failed to save to file"
					   , u"Saving failed", 0)