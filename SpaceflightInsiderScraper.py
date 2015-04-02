__author__ = 'ariky'

import httplib2
import urllib
from BeautifulSoup import BeautifulSoup
from DateUtils import toMonthNumber


def scrapeSpcaflightInsider():
    h = httplib2.Http(".cache")
    (resp_headers, content) = h.request("http://www.spaceflightinsider.com/launch-schedule/", "GET")
    soup = BeautifulSoup(content)
    tableList = soup.findAll('table', {'class': "launchcalendar"})
    for element in tableList:
        date = element.contents[1].th.text
        if 'TBD' in date:
            continue
        (month, day) = date.split(' ')
        month = toMonthNumber(month)
        print month, day
