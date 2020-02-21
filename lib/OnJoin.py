import os
import codecs

ScriptName = "Xailran's Script Bundle"
JoinedUserPath = os.path.join(os.path.dirname(__file__), "..\joinedusers.txt")
#All users who have joined the stream before
JoinedUsers = set()

def LoadJoinedUsers(Parent):
	if os.path.exists(JoinedUserPath):
		global JoinedUsers
		with codecs.open(JoinedUserPath, encoding="utf-8-sig", mode="r") as file:
			Item = [line.strip() for line in file]
			for user in Item:
				JoinedUsers.add(user)

def PointGiving(Parent, MySet):
	"""Checks if users have given points before and if they have watched the stream before. If not, gives points"""
	global JoinedUsers
	userlist = set(Parent.GetViewerList())
	newlyjoined = {}
	joining = userlist.difference(JoinedUsers)
	JoinedUsers = JoinedUsers.union(joining)
	for user in joining:
		newlyjoined[user] = MySet.joinpoints
		message = MySet.joinlogmessage.format(user, MySet.joinpoints, Parent.GetCurrencyName())
		Parent.Log(ScriptName, message)
	failedusers = Parent.AddPointsAll(newlyjoined)
	if failedusers:
		for user in failedusers:
			message = "Failed to give {1} {2} to {0}".format(user, MySet.joinpoints, Parent.GetCurrencyName())
			Parent.Log(ScriptName, message)

def SaveJoinedUsers():
	global JoinedUsers
	if len(JoinedUsers) > 0:
		with codecs.open(JoinedUserPath, "w", "utf-8") as f:
			collection = JoinedUsers.pop()
			for user in JoinedUsers:
				collection += "\r\n" + user
			f.write(collection)
