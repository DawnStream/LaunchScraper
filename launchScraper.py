#!/usr/bin/python
# -*- coding: utf-8 -*-

def toFullMonthName (month):
    if (month == 'Aug.'):
        return 'August'
    if (month == 'Sept.'):
        return 'September'
    if (month == 'Oct.'):
        return 'October'
    if (month == 'Nov.'):
        return 'November'
    if (month == 'Dec.'):
        return 'December'
    return month

print "Hello, Python!";
import httplib2
from BeautifulSoup import BeautifulSoup
h = httplib2.Http(".cache")
(resp_headers, content) = h.request("http://spaceflightnow.com/launch-schedule/", "GET")
soup = BeautifulSoup(content)
list = soup.findAll('div', {'class' : "datename"})
#print list[0].findNextSibling()
for element in list:
     date = element.contents[0].string
     if date == 'TBD':
       continue
     if ' ' not in date:
       continue
     (month, day) = date.split(' ')
     try:
        if ('/' in day or  int(day) > 31):
            continue
     except ValueError:
        continue
     month = toFullMonthName(month)

     (rocket, mission) =  element.contents[1].string.split(unicode(u' • '))
     mission = mission.replace('&amp;', '&')
     print month, day
     print rocket,':', mission

