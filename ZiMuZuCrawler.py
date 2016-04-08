import sys
import re
import requests
import time
import datetime
import json
from bs4 import BeautifulSoup
import os
import io
import codecs

TARGET_DEFINITIONS = ["HR-HDTV"]

print(datetime.datetime.now())

user = requests.Session()
userInfo = {
	'account': 'yourAccount',
  'password': 'yourPassword',
  'url_back': 'http://www.zimuzu.tv/user/user'
}
headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }

r = user.post("http://www.zimuzu.tv/user/login/ajaxLogin", data=userInfo, headers=headers)
loginInfo = json.loads(r.text)

if loginInfo['status'] == 1:
	print("Login successfully: " + userInfo['account'])

today = int(str(datetime.date.today()).split('-')[2])

file_read = open('/Users/donggeliu/kit/ZiMuZu/ZiMuZuHistory', 'r', encoding="utf-8")
lines = file_read.readlines()
file_read.close()


if lines[0][:-1] != str(today):
	s = user.get("http://www.zimuzu.tv/user/sign")

	count = 15
	while(count>0):
		print(str(count) + '\tseconds before sign in')
		count = count - 1
		time.sleep(1)

	t = user.post("http://www.zimuzu.tv//user/sign/dosign", headers=headers)
	attendanceInfo = json.loads(t.text)
	if attendanceInfo['status'] == 0:
		print(str(attendanceInfo['status']) + "\t" + "Already Signed In")
	if attendanceInfo['status'] == 1:
		print(str(attendanceInfo['status']) + "\t" + "Signed In Successfully")
	if attendanceInfo['status'] != 0 and attendanceInfo['status'] != 1:
		print(str(attendanceInfo['status']) + "\t" + "Failed")
		print(str(attendanceInfo['status']) + "\t" + attendanceInfo['info'] + str(attendanceInfo['data']))
	lines[0] = str(today) + '\n'




schedule = user.get('http://www.zimuzu.tv/tv/eschedule')
schedulePage = schedule.text
scheduleSoup = BeautifulSoup(schedulePage, "html.parser")
scheduledShows = scheduleSoup.find_all('dl')[today].find_all('dd')
scheduledShows.extend(scheduleSoup.find_all('dl')[today-1].find_all('dd'))
# scheduledShows.extend(scheduleSoup.find_all('dl')[today-2].find_all('dd'))

ScheduledToday = []
targetShows = []

for i in range(0,len(scheduledShows)):

	# Full Name
	fullName = scheduledShows[i].a.get('title')

	ScheduledToday.append(scheduledShows[i].get_text().split())
		
	# Season & Episode
	SeasonEpisode = ScheduledToday[i][1]

	# English Name
	ENGName = str(scheduledShows[i].a.get('title')).split(str(ScheduledToday[i][0]))[1]

	# # Chinese Name
	# CHNName = ScheduledToday[i][0]

	ENGName = re.sub(' ','.',ENGName)
	ENGName = re.sub("'",'',ENGName)

	targetShows.append([ENGName,SeasonEpisode])
# print(targetShows)


releasedToday = user.get('http://www.zimuzu.tv/today')
releasedTodayPage = releasedToday.text
releasedTodaySoup = BeautifulSoup(releasedTodayPage, "html.parser")
releasedTodayShows = releasedTodaySoup.find_all('div')[19].find_all('tr')
showItems = []
for i in range(1, len(releasedTodayShows)):
	# print(releasedTodayShows[i].a.string)
	definition = releasedTodayShows[i].find_all("td")[1].string
	if definition in TARGET_DEFINITIONS:
		releasedTodayShowName = releasedTodayShows[i].a.string
		links = releasedTodayShows[i].find_all("td")[3].find_all('a')
		for i in range(0,len(links)):
			if links[i].string.encode("utf-8") == '驴'.encode("utf-8"):
				preferredLink = links[i].get('href').encode("utf-8")
				showItems.append([releasedTodayShowName, preferredLink])
				break
			# if links[i].string.encode("utf-8") == '磁'.encode("utf-8"):
			# 	preferredLink = links[i].get('href').encode("utf-8")
			# 	showItems.append([releasedTodayShowName, preferredLink])
			# 	break
			if links[i].string.encode("utf-8") == '迅'.encode("utf-8"):
				preferredLink = links[i].get('href').encode("utf-8")
				showItems.append([releasedTodayShowName, preferredLink])
				break

# print(showItems)

for m in range(0, len(targetShows)):
	for n in range(0, len(showItems)):
		if (re.search(targetShows[m][0], showItems[n][0], re.IGNORECASE) and re.search(targetShows[m][1], showItems[n][0], re.IGNORECASE)):
			# print(showItems[n][0])
			exists = False
			for line in lines:
				if re.search(targetShows[m][0], line, re.IGNORECASE):
					if not re.search(targetShows[m][1], line, re.IGNORECASE):
						lines.remove(line)
						line = showItems[n][0] + "\n"
					else:
						exists = True
			if not exists:
				print(targetShows[m][0])
				lines.append(showItems[n][0]+ "\n")
				os.system('open /Applications/Thunder.app '  + '"' + showItems[n][1].decode(encoding='UTF-8') + '"')
				time.sleep(5)



file_write = open('/Users/donggeliu/kit/ZiMuZu/ZiMuZuHistory', 'w', encoding="utf-8")
file_write.writelines(lines)
file_write.close()
print("Quit Successfully")



