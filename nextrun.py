#! /usr/bin/python
import random
import datetime


backup_start_day = random.choice(['1', '2', '3', '4', '5', '6', '7'])
nday = datetime.timedelta(days = int(backup_start_day))
nextrun = datetime.datetime.now() + datetime.timedelta(days = int(backup_start_day))
print (backup_start_day)
print(datetime.date.isoformat(nextrun))
#print(nday.seconds())

#now = datetime.datetime.day(backup_start_day)
#print now.strftime("%d")

#print(datetime.datetime.weekday(7))
#print(datetime.datetime.today())
#datetime.datetime(2012, 3, 23, 23, 24, 55, 173504)
#datetime.datetime.today().weekday()
