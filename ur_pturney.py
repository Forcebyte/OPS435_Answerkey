#!/usr/bin/env python3
'''
   authorship declaration

   __author__ Patrick Turney
   __date__ March 2018
   __version__ 0.1
 
   OPS435 Assignment 2 - Fall 2018
	Program: ur_pturney.py
	Author: "Patrick Turney"
	The python code in this file ur_pturney.py is original work written by
	"Patrick Turney". No code in this file is copied from any other source 
	including any person, textbook, or on-line resource except those provided
	by the course instructor. I have not shared this python file with anyone
	or anything except for submission for grading.  
	I understand that the Academic Honesty Policy will be enforced and violators 
	will be reported and appropriate action will be taken.
'''

import os 
import sys
import time

from time import strftime
def parse_time(s):
    hour, min, sec = s.split(':')
    try:
        hour = int(hour)
        min = int(min)
        sec = int(sec)
    except ValueError:
        # handle errors here, but this isn't a bad default to ignore errors
        return 0
    return hour * 60 * 60 + min * 60 + sec

def get_login_rec(login_recs,args):
	''' docstring for this fucntion
	get records from the last command
	filter out the unwanted records
	add filtered record to list (login_recs)'''
	#[ put your python code for this function here ]
	#return login_recs

	#Grab the Argument given, either user (wants the users logged in) or host (wants the host IP)
	argument = str(args.list)

	#If the argument is asking for the user list, run through and give users
	if "user" in argument:
		users = []
		#Grab each user for each line
		for item in login_recs:
			#split on each column, then grab first column
			split = item.split()
			user = split[0]
			#If it is unique, add it to users
			if user not in users:
				users.append(user)
		return(users)
	
	#If the argument is asking for the host list, run through and give hosts
	if "host" in argument:
		hosts = []
		for item in login_recs:
			split = item.split()
			host = split[2]
			if host not in hosts:
				hosts.append(host)
		return(hosts)

def read_login_rec(filelist,args):
	''' docstring for this function
	get records from given filelist
	open and read each file from the filelist
	filter out the unwanted records
	add filtered record to list (login_recs)'''
	#[ put your python code for this function here ]

	#If we're just given one file, add it to a single array
	if isinstance(filelist, str):
			filelist = [filelist]
	#Takes each record from filelist, adds it to a list
	unfiltered = []

	#Read the record
	for fileitem in filelist:
			file = open(fileitem,"r")
			unfiltered.extend(file.read().splitlines())

	#If there is an rhost argument (filter by IP), we filter by IP and add it to filtered
	# If there isn't just set filtered to be unfiltered for future filtering
	filtered = []
	if args.rhost is not None:
		rhost = str(args.rhost)
		for item in unfiltered:
				if rhost in item:
						filtered.append(item)
	else:
		filtered = unfiltered
	#If there is a user argument (filter by username), we filter by the username and add it
	#To the filteredfinal list, if there isn't, just set filtered to be filteredfinal and return
	filteredfinal = []
	if args.user is not None:
		username = str(args.user)
		for item in filtered:
				if username in item:
						filteredfinal.append(item)
	else:
			filteredfinal = filtered
	login_rec = filteredfinal
	return login_rec


def cal_daily_usage(subject,login_recs):
	''' docstring for this function
	generate daily usage report for the given 
	subject (user or remote host)'''
	#[ put your python code for this function here ]
	#return daily_usage
	timedict = {}
	for item in login_recs:
		#Split item into catagories
		split = item.split()

		timestart = split[6]
		timeend = split[12]

		#Parse time takes a 
		timestartsec = parse_time(str(timestart))
		timeendsec = parse_time(str(timeend))

		timedelta = timeendsec - timestartsec

		#String is as follows...
		#SPLIT[7] = Year YYYY
		#SPLIT[4] = Month (Apr)
		#SPLIT[5] = Day DD

		#Since we can't use datetime, convert the month spelling to a number
		dictmonth = {"Jan":"1", "Feb":"2","Mar":"3","Apr":"4","May":"5","Jun":"6","Jul":"7","Aug":"8","Sep":"9","Oct":"10","Nov":"11","Dec":"12"}
		month = str(split[4])
		month = dictmonth.get(month)
		dateobject = str(split[7]) + " " + month + " " + str(split[5])
		dateobjectstring = str(dateobject)
		if dateobject in timedict:
			oldtime = timedict[dateobjectstring]
			newtime = timedelta + int(oldtime)
			timedict[dateobjectstring] = newtime
			#timedict[str(dateobject)] = [timedict[str(dateobject)], str((timedelta + int(timedict.get(str(dateobject)))))]
		else:
			#minhour = str(split[-1])
			timedict[dateobjectstring] = str(timedelta)
	return(timedict)

def cal_weekly_usage(subject,login_recs):
	''' docstring for this function
	generate weekly usage report for the given 
	subject (user or remote host)'''
	#[ put your python code for this function here ]
	#return weekly_usage
	timedict = {}
	for item in login_recs:
		#Split item into catagories
		split = item.split()

		timestart = split[6]
		timeend = split[12]

		#Parse time gets the number of seconds in a date statement
		timestartsec = parse_time(str(timestart))
		timeendsec = parse_time(str(timeend))

		timedelta = timeendsec - timestartsec

		#String is as follows...
		#SPLIT[7] = Year YYYY
		#SPLIT[4] = Month (Apr)
		#SPLIT[5] = Day DD

		
		dateobject = str(split[7]) + " " + str(split[4]) + " " + str(split[5])
		striptime = time.strptime(dateobject, "%Y %b %d")
		weeknum = str(strftime("%U", striptime))
		weeknum = str(int(weeknum) + 1)

		dateobjectstring = split[7] + " " + weeknum
		if dateobjectstring in timedict:
			oldtime = timedict[dateobjectstring]
			newtime = timedelta + int(oldtime)
			timedict[dateobjectstring] = newtime
			#timedict[str(dateobject)] = [timedict[str(dateobject)], str((timedelta + int(timedict.get(str(dateobject)))))]
		else:
			#minhour = str(split[-1])
			timedict[dateobjectstring] = str(timedelta)
	return(timedict)

def cal_monthly_usage(subject,login_recs):
	''' docstring for this function
	generate monthly usage report fro the given
	subject (user or remote host)'''
	#[ put your python code for this function here ]
	#return monthly_usage
	timedict = {}
	for item in login_recs:
		#Split item into catagories
		split = item.split()

		timestart = split[6]
		timeend = split[12]

		#Parse time gets the number of seconds in a date statement
		timestartsec = parse_time(str(timestart))
		timeendsec = parse_time(str(timeend))

		timedelta = timeendsec - timestartsec

		#String is as follows...
		#SPLIT[7] = Year YYYY
		#SPLIT[4] = Month (Apr)
		#SPLIT[5] = Day DD

		#Since we can't use datetime, convert the month spelling to a number
		dictmonth = {"Jan":"1", "Feb":"2","Mar":"3","Apr":"4","May":"5","Jun":"6","Jul":"7","Aug":"8","Sep":"9","Oct":"10","Nov":"11","Dec":"12"}
		month = str(split[4])
		month = dictmonth.get(month)

		dateobject = str(split[7]) + " " + str(split[4]) + " " + str(split[5])
		dateobjectstring = split[7] + " " + month
		if dateobjectstring in timedict:
			oldtime = timedict[dateobjectstring]
			newtime = timedelta + int(oldtime)
			timedict[dateobjectstring] = newtime
			#timedict[str(dateobject)] = [timedict[str(dateobject)], str((timedelta + int(timedict.get(str(dateobject)))))]
		else:
			#minhour = str(split[-1])
			timedict[dateobjectstring] = str(timedelta)
	return(timedict)




	 
if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-F", "--file", help="list of files to be processed")
	parser.add_argument("-l", "--list",  help="generate user name or remote host IP from the given files", nargs=2)
	parser.add_argument("-r", "--rhost",  help="usage report for the given remote host IP")
	parser.add_argument("-t", "--type",  help="type of report: daily, weekly, and monthly", nargs=2)
	parser.add_argument("-u", "--user", help="usage report for the given user name")
	parser.add_argument("-v", "--verbose", help="turn on output verbosity")
	#[ code to retrieve command line argument using the argparse module 
	args = parser.parse_args()

	#If there are arguments
	if args is not None:
		#If running with -l (E.g. ./ur.py -l user/host test.txt)
		if args.list is not None:
			#Since we are running with -l, the file that we are using is specified in the fourth argument
			args.file = [str(sys.argv[3])]
			login_rec = read_login_rec(args.file,args)
			userhost_rec = get_login_rec(login_rec,args)
			#Now that we are done, print the user or host involved by passing through each host/user in the list
			for user_or_host in userhost_rec:
				print(user_or_host)
		
		#If running with -r (E.g. ./ur.py -r 10.0.0.1 test.txt)
		if args.rhost or args.user is not None:
			#Grab the bulk file, and parse it
			args.file = [str(sys.argv[5])]
			login_rec = read_login_rec(args.file,args)
			
			#In this case, the timeframe will be what the user wants
			timeframe = str(sys.argv[4])


			subject = str(sys.argv[2])

			#If asking for a daily report (E.g. ./ur.py -r 10.0.0.1 daily test.txt)
			if "daily" in timeframe:
				#Grab the ditionary for daily usage
				daily_dict 	= cal_daily_usage(subject,login_rec)

				line = "Daily Usage Report for " + str(subject)
				eq = len(line)
				
				print(line)
				print("=" * eq)
				print("%-15s %-15s" %("Date","Usage in Seconds"))
				total = 0

				for key, value in daily_dict.items():
					#print(str(key) + "	" + str(value))
					print("%-10s %-10s" %(str(key),"    " + str(value)))
					total = total + value
				print("%-10s %-10s" %("Total","    " + str(total)))

			#If asking for a weekly report (E.g. ./ur.py -r 10.0.0.1 weekly test.txt)
			if "weekly" in timeframe:
				weekly_dict = cal_weekly_usage(subject,login_rec)

				line = "Weekly Usage Report for " + str(subject)
				eq = len(line)
				
				print(line)
				print("=" * eq)
				print("%-15s %-15s" %("Week #","Usage in Seconds"))
				total = 0

				for key, value in weekly_dict.items():
					#print(str(key) + "	" + str(value))
					print("%-10s %-10s" %(str(key),"    " + str(value)))
					total = total + value
				print("%-10s %-10s" %("Total","    " + str(total)))

			#If asking for a monthly report (E.g. ./ur.py -r 10.0.0.1 monthly test.txt)
			if "monthly" in timeframe:
				monthly_dict = cal_monthly_usage(subject,login_rec)
				print(monthly_dict)

				line = "Monthly Usage Report for " + str(subject)
				eq = len(line)
				
				print(line)
				print("=" * eq)
				print("%-15s %-15s" %("Month","Usage in Seconds"))
				total = 0

				for key, value in monthly_dict.items():
					#print(str(key) + "	" + str(value))
					print("%-10s %-10s" %(str(key),"    " + str(value)))
					total = total + value
				print("%-10s %-10s" %("Total","    " + str(total)))

			
	#[ based on the command line option, generate and print
	#  the requested usage report ]