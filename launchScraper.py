#!/usr/bin/python
# -*- coding: utf-8 -*-

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']


def toFullMonthName(month):
    if month == 'Aug.':
        return 'August'
    if month == 'Sept.':
        return 'September'
    if month == 'Oct.':
        return 'October'
    if month == 'Nov.':
        return 'November'
    if month == 'Dec.':
        return 'December'
    return month


def toMonthNumber(month):
    return months.index(month) + 1


print "Hello, Python!"
import re
import json
import httplib2
from BeautifulSoup import BeautifulSoup

h = httplib2.Http(".cache")
(resp_headers, content) = h.request("http://spaceflightnow.com/launch-schedule/", "GET")
soup = BeautifulSoup(content)
divList = soup.findAll('div', {'class': "datename"})
# print list[0].findNextSibling()
for element in divList:
    date = element.contents[0].string
    if date == 'TBD':
        continue
    if ' ' not in date:
        continue
    (month, day) = date.split(' ')
    try:
        if '/' in day or int(day) > 31:
            continue
    except ValueError:
        continue
    month = toMonthNumber(month)

    (rocket, mission) = element.contents[1].string.split(unicode(u' • '))
    mission = mission.replace('&amp;', '&')
    time = element.findNextSibling().contents[1]
    if 'TBD' in time:
        startTime = '00:00'
        endTime = ''
    else:
        time = time.split(' GMT')[0]
        time = time.split('-')
        startTime = time[0].lstrip()
        m = re.search('(\d\d)(\d\d)(\d\d)?', startTime)
        startTime = m.group(1) + ':' + m.group(2)
        if len(time) > 1:
            endTime = time[1].lstrip()
            m = re.search('(\d\d)(\d\d)(\d\d)?', endTime)
            endTime = m.group(1) + ':' + m.group(2)
        else:
            endTime = ''

    print rocket, ':', mission
    print startTime, endTime
    print month, day

    iso = '2015' + '-' + '{:0>2}'.format(str(month)) + '-' + '{:0>2}'.format(str(day)) + 'T' + str(startTime) + 'Z'
    body = json.dumps({'date': iso})
    headers = {'Content-type': 'application/json'}
    h.request("http://localhost:3000/testDate/", 'POST', headers=headers, body=body)


