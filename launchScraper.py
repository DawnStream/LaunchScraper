#!/usr/bin/python

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
 print month, day

