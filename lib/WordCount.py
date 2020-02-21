import json
import re
import os
import codecs

userwordcountfile = os.path.join(os.path.dirname(__file__), r"..\wordcounts.txt")
emoteList = set()
userwordcount = {}

#---------------------------------------
#   Word Count Functions
#---------------------------------------
def EmoteList(Parent):
	"""Grab the list of available Twitch emotes"""
	global emoteList
	jsonData = json.loads(Parent.GetRequest("https://twitchemotes.com/api_cache/v3/global.json", {}))
	if jsonData["status"] == 200:
		emoteList.update(set(json.loads(jsonData["response"]).keys()))

		# Grab the list of available Twitch emotes of the users channel
		jsonData = json.loads(Parent.GetRequest("https://decapi.me/twitch/subscriber_emotes/" + Parent.GetChannelName(), {}))
		if jsonData["status"] == 200:
			tempEmoteNames = jsonData["response"].split(" ")
			if tempEmoteNames[0] != "This": #channel has no sub button or sub button + no emotes
				emoteList.update(set(tempEmoteNames))

	# Grab the list of available BetterTwitchTV emotes on the users channel
	jsonData = json.loads(Parent.GetRequest("https://api.betterttv.net/2/channels/" + Parent.GetChannelName(), {}))
	if jsonData["status"] == 200:
		for emote in json.loads(jsonData["response"])["emotes"]:
			emoteList.add(emote['code'])

	# Grab the list of available global BetterTwitchTV emotes
	jsonData = json.loads(Parent.GetRequest("https://api.betterttv.net/2/emotes", {}))
	if jsonData["status"] == 200:
		for emote in json.loads(jsonData["response"])["emotes"]:
			emoteList.add(emote['code'])

	# Grab the list of available FFZ emotes	on user channel
	jsonData = json.loads(Parent.GetRequest("https://decapi.me/ffz/emotes/" + Parent.GetChannelName(), {}))
	if jsonData["status"] == 200:
		tempEmoteNames = jsonData["response"].split(" ")
		if tempEmoteNames[0] != "Not": #channel has no emotes
			emoteList.update(set(tempEmoteNames))

def LoadWordCounts():
	"""Loads user word count totals from existing data"""
	global userwordcount
	if not os.path.exists(userwordcountfile):
		userwordcount = {}
		return
	with codecs.open(userwordcountfile, encoding="utf-8-sig", mode="r") as file:
		Item = [line.strip() for line in file]
		if not Item:
			userwordcount = {}
			return
		for x in Item:
			#data[0] = username, data[1] = words, data[2] = emotes. data[3] = numbers, data[4] = commands, data [5] = commands
			data = x.split()
			userdata = {"wordcount":int(data[1]),"emotecount":int(data[2]),"numbercount":int(data[3]),"commandcount":int(data[4])}
			if len(data) == 6:
				userdata["messagecount"] = int(data[5])
			else:
				userdata["messagecount"] = 0
			userwordcount[data[0]] = userdata

def SaveWordCounts():
	"""Saves user word count totals from existing data"""
	global userwordcount
	if not userwordcount:
		return
	with codecs.open(userwordcountfile, "w", "utf-8") as file:
		userdata = userwordcount.popitem()
		filedata = userdata[0] + " " + str(userdata[1]["wordcount"]) + " " + str(userdata[1]["emotecount"]) + " " + str(userdata[1]["numbercount"]) + " " + str(userdata[1]["commandcount"]) + " " + str(userdata[1]["messagecount"])
		for key in userwordcount:
			filedata += "\r\n" + key + " " + str(userwordcount[key]["wordcount"]) + " " + str(userwordcount[key]["emotecount"]) + " " + str(userwordcount[key]["numbercount"]) + " " + str(userwordcount[key]["commandcount"]) + " " + str(userwordcount[key]["messagecount"])
		file.write(filedata)

def CollectWords(data, MySet):
	"""Counts words"""
	global userwordcount
	#MySet.countcommands for whether or not to count messages counting a command
	messagecount = 1
	wordcount = int(data.GetParamCount())
	emotecount = 0
	numbercount = 0
	commandcount = 0
	#Checks if command
	if data.GetParam(0).startswith("!"):
		if MySet.countCommands:
			commandcount = 1
		#If not counting commands, ditches message
		else:
			return
	#If countemotes is true, recognized emotes will be counted and subtracted from word count. If not, all emotes will be counted as words
	for x in range(0, data.GetParamCount()):
		userstring = data.GetParam(x)
		if MySet.countEmotes and userstring in emoteList:
			emotecount += 1
		else:
			try:
				int(userstring)
			except:
				pass
			else:
				if MySet.countNumbers:
					numbercount += 1
	wordcount -= (numbercount + emotecount + commandcount)
	if data.UserName.lower() in userwordcount:
		userwordcount[data.UserName.lower()]["wordcount"] += wordcount
		userwordcount[data.UserName.lower()]["emotecount"] += emotecount
		userwordcount[data.UserName.lower()]["numbercount"] += numbercount
		userwordcount[data.UserName.lower()]["commandcount"] += commandcount
		userwordcount[data.UserName.lower()]["messagecount"] += messagecount
	else:
		userdata = {}
		userdata["wordcount"] = wordcount
		userdata["emotecount"] = emotecount
		userdata["numbercount"] = numbercount
		userdata["commandcount"] = commandcount
		userdata["messagecount"] = messagecount
		userwordcount[data.UserName.lower()] = userdata
	
def Parameters(parseString, userid, username, targetid, targetname, message, MySet):
	tw = re.search(r"\$topwords\((\d+)\)", parseString)
	tm = re.search(r"\$topmessages\((\d+)\)", parseString)
	if tw:
		entries = WordLeaderboard(int(tw.group(1)), MySet)
		parseString = parseString.replace(tw.group(0), entries)
	if tm:
		entries = MessageLeaderboard(int(tm.group(1)), MySet)
		parseString = parseString.replace(tm.group(0), entries)
	if targetname != "":
		user = targetname.lower()
	else:
		user = username.lower()
	if "$wordpos" in parseString:
		parseString = parseString.replace("$wordpos", WordPosition(MySet, user))
	if "$messagepos" in parseString:
		parseString = parseString.replace("$messagepos", MessagePosition(MySet, user))
	if user in userwordcount:
		parseString = parseString.replace("$wordcount", str(userwordcount[user]["wordcount"]))
		parseString = parseString.replace("$emotecount", str(userwordcount[user]["emotecount"]))
		parseString = parseString.replace("$numbercount", str(userwordcount[user]["numbercount"]))
		parseString = parseString.replace("$commandcount", str(userwordcount[user]["commandcount"]))
		parseString = parseString.replace("$messagecount", str(userwordcount[user]["messagecount"]))
	return parseString

def WordLeaderboard(value, MySet):
	"""Creates a leaderboard with "value" entries, based on the $wordcount of each user"""
	nameleaderboard = []
	wordleaderboard = []
	leaderboarddict = {}
	ExclusionList = MySet.countExclusionList.lower().split()
	for x in userwordcount:
		leaderboarddict[x] = userwordcount[x]["wordcount"] + userwordcount[x]["emotecount"] + userwordcount[x]["numbercount"] + userwordcount[x]["commandcount"]
	while (len(nameleaderboard) < value and len(nameleaderboard) < len(leaderboarddict)):
		topuser = ""
		topvalue = 0
		for key in leaderboarddict:
			if leaderboarddict[key] > topvalue and key not in nameleaderboard and key.lower() not in ExclusionList:
				topuser = key
				topvalue = leaderboarddict[key]
		nameleaderboard.append(topuser)
		wordleaderboard.append(topvalue)
		if len(nameleaderboard) == value:
			break
	entries = "#1 " + nameleaderboard.pop(0) + " (" + str(wordleaderboard.pop(0)) + ")"
	for x in range(0, len(nameleaderboard)):
		if wordleaderboard[x] == 0:
			break
		entries += " - #" + str(x + 2) + " " + nameleaderboard[x] + " (" + str(wordleaderboard[x]) + ")"
	return entries

def MessageLeaderboard(value, MySet):
	"""Creates a leaderboard with "value" entries, based on the $messagecount of each user"""
	nameleaderboard = []
	wordleaderboard = []
	leaderboarddict = {}
	ExclusionList = MySet.countExclusionList.lower().split()
	for x in userwordcount:
		leaderboarddict[x] = userwordcount[x]["messagecount"]
	while len(nameleaderboard) < value and len(nameleaderboard) < len(leaderboarddict):
		topuser = ""
		topvalue = 0
		for key in leaderboarddict:
			if leaderboarddict[key] > topvalue and key not in nameleaderboard and key.lower() not in ExclusionList:
				topuser = key
				topvalue = leaderboarddict[key]
		nameleaderboard.append(topuser)
		wordleaderboard.append(topvalue)
	entries = "#1 " + nameleaderboard.pop(0) + " (" + str(wordleaderboard.pop(0)) + ")"
	for x in range(0, len(nameleaderboard)):
		if wordleaderboard[x] == 0:
			break
		entries += " - #" + str(x + 2) + " " + nameleaderboard[x] + " (" + str(wordleaderboard[x]) + ")"
	return entries

def WordPosition(MySet, user):
	"""Creates a leaderboard with "value" entries, based on the $wordcount of each user"""
	leaderboarddict = {}
	ExclusionList = MySet.countExclusionList.lower().split()
	if user.lower() in ExclusionList:
		return "#0"
	for x in userwordcount:
		leaderboarddict[x] = userwordcount[x]["wordcount"] + userwordcount[x]["emotecount"] + userwordcount[x]["numbercount"] + userwordcount[x]["commandcount"]
	count = 0
	while len(leaderboarddict) != 0:
		count += 1
		topuser = ""
		topvalue = 0
		for key in leaderboarddict:
			if leaderboarddict[key] > topvalue:
				topuser = key
				topvalue = leaderboarddict[key]
		if topuser == user:
			return "#" + str(count)
		if topuser.lower() in ExclusionList:
			count -= 1
		leaderboarddict.pop(topuser)
	return "Not Found"

def MessagePosition(MySet, user):
	"""Creates a leaderboard with "value" entries, based on the $wordcount of each user"""
	leaderboarddict = {}
	ExclusionList = MySet.countExclusionList.lower().split()
	if user.lower() in ExclusionList:
		return "#0"
	for x in userwordcount:
		leaderboarddict[x] = userwordcount[x]["messagecount"]
	count = 0
	while len(leaderboarddict) > 0:
		count += 1
		topuser = ""
		topvalue = -1
		for key in leaderboarddict:
			if leaderboarddict[key] > topvalue:
				topuser = key
				topvalue = leaderboarddict[key]
		if topuser == user:
			return "#" + str(count)
		if topuser.lower() in ExclusionList:
			count -= 1
		leaderboarddict.pop(topuser)
	return "Not Found"