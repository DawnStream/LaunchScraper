__author__ = 'ariky'

import httplib2
import urllib
import re
import json
from BeautifulSoup import BeautifulSoup
from DateUtils import toMonthNumber


def scrapeSpcaflightInsider():
    h = httplib2.Http(".cache")
    (resp_headers, content) = h.request("http://www.spaceflightinsider.com/launch-schedule/", "GET")
    soup = BeautifulSoup(content)
    # noinspection PyPep8Naming
    tableList = soup.findAll('table', {'class': "launchcalendar"})
    # print tableList[2].prettify()
    # print tableList[2].contents[1].contents[3]
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
        # noinspection PyPep8Naming
        rocketVersion = rocket.split(' ')
        if len(rocketVersion) > 2:
            version = rocketVersion[2]
            rocket = rocketVersion[0] + ' ' + rocketVersion[1]
        elif len(rocketVersion) > 1:
            version = rocketVersion[1]
            rocket = rocketVersion[0]
        else:
            # noinspection PyPep8Naming
            rocketVersion = re.search('(Soyuz)-(\w+)', rocket)
            if rocketVersion is not None:
                rocket = rocketVersion.group(1)
                version = rocketVersion.group(2)
            else:
                version = ''
        location = element.contents[2].table.contents[1].contents[3].text
        time = element.contents[2].table.contents[2].contents[3].text
        if 'TBD' in time:
            # noinspection PyPep8Naming
            startTime = '00:00'
            # noinspection PyPep8Naming
            endTime = ''
        else:
            t = re.search('(\d\d?):(\d+) ([AP]M) [\w]{3} \(UTC([-+]\d+)', time)
            # noinspection PyPep8Naming
            startTime = int(t.group(1))
            if 'PM' in t.group(3):
                startTime += 12
            startTime -= int(t.group(4))
            # noinspection PyPep8Naming
            startTime = str(startTime) + ':' + t.group(2)
            # noinspection PyPep8Naming
            endTime = ''
        start_iso = '2015' + '-' + '{:0>2}'.format(str(month)) + '-' + '{:0>2}'.format(str(day)) + 'T' + str(
            startTime) + 'Z'
        end_iso = '2015' + '-' + '{:0>2}'.format(str(month)) + '-' + '{:0>2}'.format(str(day)) + 'T' + str(
            endTime) + 'Z'
        print mission
        print start_iso
        print end_iso
        print location
        print rocket
        print version
        # noinspection PyPep8Naming
        (resp_headers, rocketResponse) = h.request('http://localhost:3000/rocket/model/' + urllib.quote(rocket))
        # noinspection PyPep8Naming
        rocketResponse = json.loads(rocketResponse)
        print rocketResponse
        if not rocketResponse:
            body = json.dumps({'Model': rocket, 'Version': version})
            headers = {'Content-type': 'application/json'}
            (resp_headers, rocket) = h.request("http://localhost:3000/rocket/", 'POST', headers=headers, body=body)
            rocket = json.loads(rocket)[0]
            print rocket
        else:
            found = False
            for response in rocketResponse:
                if version in response['Version']:
                    rocket = response
                    found = True
                    break
            if not found:
                body = json.dumps({'Model': rocket, 'Version': version})
                headers = {'Content-type': 'application/json'}
                (resp_headers, rocket) = h.request("http://localhost:3000/rocket/", 'POST', headers=headers, body=body)
                rocket = json.loads(rocket)[0]
                print rocket
        launch = {'Mission': mission, 'Date': start_iso, 'Rocket': rocket, 'Location': location}
        print json.dumps(launch)
        body = json.dumps(launch)
        headers = {'Content-type': 'application/json'}
        (resp_headers, rocket) = h.request("http://localhost:3000/launch/", 'POST', headers=headers, body=body)


