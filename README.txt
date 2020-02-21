#######################################
#   Xailran's Script Bundle Script    #
#######################################

Description: A collection of modules to enhance your stream
Made By: Xailran
Website: https://www.twitch.tv/xailran
	 https://www.twitter.com/xailran

#####################
#     Versions      #
#####################

1.3.3 - Improved user customization settings
1.3.2 - Song encoding will now identify if the song was in the playlist or requested, and will treat it accordingly
1.3.1 - Fixed issues with nextsong, and changed it to be a parameter, rather than a built in command
1.3.0 - Added exclusion list for word/message leaderboard. Added $number, $interrupt, $filelines, and $deleteline parameters!
1.2.1 - Bug fixes for next song and word count modules
1.2.0 - Added $delay parameter
1.1.0 - Added word count parameters
1.0.0 - Initial Release

Known bugs:
	Encoded Songs
If two or more faulty songs are played in a row, the script will not detect the songs properly

#####################
#       Usage       #
#####################
Next Songs - This module is for being able to list x upcoming songs without looking at or setting up the songlist url.
$songs(songcount) - Lists next "soungcount" songs.

Points On Join - This module will automatically give first time viewers x amount of points when they first join the stream

Encoded Songs - This module will automatically detect when a song has not played properly, and will send a message to chat and refund points for the song request to the requester

Songlist Exporter - This module takes your current playlist and saves all the urls to a .txt file (which you set in the UI)

Word Count Parameters - This module counts users have said the most words or messages, and forms that into a leaderboard. Also has parameters for individual user stats.
$topwords(num) = Lists the top x users, based on combined word, number, emote and command count.
$topmessages(num) = Lists the top x users, based on the amount of messages they have sent.
$wordpos = Gives position of the user/target on the word leaderboard
$messagepos = Gives position of the user/target on the word leaderboard
$wordcount = total words said, excluding commands, emotes, and numbers counted
$emotecount = total emotes used in chat
$numbercount = total amount of numbers used in chat (Counts "5", does not count "five")
$commandcount = total amount of commands used in chat (based off having a "!" at the front, does not check if it is actually a command)
$messagecount = total amount of messages sent in chat.

Example command:
"$tousername is in position $messagepos with $messagecount messages. Those messages have contained a total of $math[$wordcount+$emotecount+$numbercount+$commandcount] words"

$delay(seconds, message) Parameter - This module allows you to add a delay into your commands. For example, if you want a message to send 3 seconds later than the first part of the command. Will not delay file related parameters, or send whispers.
Example command:
"This will send straight away $delay(5, This will send 5 seconds later) $delay(10, This 3rd message will be sent 10 seconds after the first message)"

$number(min, max, number, "success message", "fail message") Parameter - Checks if "number" is between "min" and "max". If it is, the success message will be returned. If not, the fail message will be returned. Will also return fail message if not all the numbers are actually numbers

$interrupt[func]tion - Use this parameter to delay a parameter from triggering! Put $interrupt[ in front of the parameter you want to delay, and put the ] somewhere inside the parameter. Example: $interrupt[$overwrit]efile("filepath", "text")

$filelines(path) Parameter - Does what it sounds like! Counts the amount of lines in a file. Path must start from drive letter (eg. "C:/")
$deleteline("path", num, "success", "fail") Parameter - Deletes line num from the file set in path. The first line in a file is line 0!

######################
#   Future Updates   #
######################
Personal uptime command (check how long user has been on channel since last bot reset) (Suggested by TOXIC)
Add !qotd feature
Track total attended streams per user
Add overlay for Next Songs module, to show x upcoming songs on stream
Announce song pos when a new song has been added to the songlist
Add total message count per stream

################################
#   Other Scripts by Xailran   #
################################
Please note that commissioned scripts come with idea and sale protection.
Sale protection means that I will not give away a script for free that someone else has paid for, without permission from the original client. Commissioning the script only gives the client the rights to use the script, not to sell or otherwise distribute the script.

Public Scripts:
Store (2.0.0)
Fight (1.3.3)
Xailran's Script Bundle (1.3.3)
Combo Counter (1.0.2)

Paid Scripts:
Stréamon (https://www.kickstarter.com/projects/xailran/streamlabs-chatbot-pokemon-script?ref=1nv8m4)
Advanced Trivia (1.4.1.1) ($15 USD)
Extra Currency (In development, $25 USD)
Leaderboard Filter ($10 USD)
Tiered Sub Payouts ($15 USD)

Up to date as of 21/02/2020

#############################################
#   Donations are never expected, but any   #
#    support definitely helps, and keeps    #
#     me able to make more free scripts!    #
#       https://streamlabs.com/xailran      # 
#############################################
#############################################
# Tag me in the Streamlabs Chatbot discord  #
#    if you have any questions or ideas!    #
#   https://discordapp.com/invite/J4QMG5m   #
#############################################