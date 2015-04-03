__author__ = 'ariky'

import httplib2
import urllib
import re
from BeautifulSoup import BeautifulSoup
from DateUtils import toMonthNumber


def scrapeSpcaflightInsider():
    h = httplib2.Http(".cache")
    (resp_headers, content) = h.request("http://www.spaceflightinsider.com/launch-schedule/", "GET")
    soup = BeautifulSoup(content)
    tableList = soup.findAll('table', {'class': "launchcalendar"})
    print tableList[2].prettify()
    print tableList[2].contents[1].contents[3]
    for element in tableList:
        date = element.contents[1].th.text
        if 'TBD' in date:
            continue
        (month, day) = date.split(' ')
        month = toMonthNumber(month)
        mission = element.contents[1].contents[3].text
        mission = mission.replace('&amp;', '&')
        m = re.search('([\s\S]+)(?= \()', mission)
        if m is not None:
            mission = m.group(0)
        rocket = element.contents[2].td.text
        rocketVersion = rocket.split(' ')
        if len(rocketVersion) > 2:
            version = rocketVersion[2]
            rocket = rocketVersion[0] + ' ' + rocketVersion[1]
        elif len(rocketVersion) > 1:
            version = rocketVersion[1]
            rocket = rocketVersion[0]
        else:
            rocketVersion = re.search('(Soyuz)-(\w+)', rocket)
            if rocketVersion is not None:
                rocket = rocketVersion.group(1)
                version = rocketVersion.group(2)
            else:
                version = ''
        location = element.contents[2].table.contents[1].contents[3].text
        time = element.contents[2].table.contents[2].contents[3].text
        if 'TBD' in time:
            startTime = '00:00'
            endTime = ''
        else:
            t = re.search('(\d\d?):(\d+) ([AP]M) [\w]{3} \(UTC([-+]\d+)', time)
            startTime = int(t.group(1))
            if 'PM' in t.group(3):
                startTime += 12
            startTime -= int(t.group(4))
            startTime = str(startTime) + ':' + t.group(2)
            endTime = ''
        iso = '2015' + '-' + '{:0>2}'.format(str(month)) + '-' + '{:0>2}'.format(str(day)) + 'T' + str(startTime) + 'Z'
        print mission
        print iso
        print location
        print rocket
        print version
        (resp_headers, rocketRespone) = h.request('http://localhost:3000/rocket/model/'+urllib.quote(rocket))
        print rocketRespone


