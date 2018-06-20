#!/usr/bin/env python

from os import path
from subprocess import call

import sys
import requests
import json
import time

if len(sys.argv) < 3:
  print("1. Find the group's URL name - the part that comes right after meetup.com/. For example, in the case of https://www.meetup.com/Blockchain-for-Funds/, it would be Blockchain-for-Funds.")
  print("")
  print("2. Go to https://secure.meetup.com/meetup_api/key/ and copy your API key.")
  print("")
  print("3. Rerun this command with the group's URL name as the second parameter and the API key as the first. For example:")
  print("{} 42ccc44912e4414b9c5d2806f74197 Blockchain-for-Funds".format(sys.argv[0]))
  sys.exit(1)

user_key = sys.argv[1]
group_name = sys.argv[2]

url="https://api.meetup.com/members?group_urlname={group_name}&sign=true&key={user_key}".format(group_name=group_name, user_key=user_key)

data = requests.get(url).json()
meta = data['meta']
results = data['results']
total = meta['total_count']
while len(results) < total:
  results += requests.get("{}&page=200&offset={}".format(url, int(len(results)/200))).json()['results']

people=results

html="""<hr>
<p><a href="{link}">{name}</a><p><img src="{photo}"/></p></p>
"""

def to_html(p):
  return html.format(link=p['link'], name=p['name'], photo=p['photo_url'])

html_output = "".join([to_html(p) for p in people])

html_file_path = path.expanduser("~/Downloads/{}.{}.html".format(group_name, int(time.time())))
html_file = open(html_file_path, 'w')
html_file.write(html_output)
html_file.close()

# call(['open', html_file_path])

def to_row(p):
  assert "".join([p['name'], p['link'], p['photo_url'], p['country'], p['city'], p['zip'] ]).find('"') == -1, 'Found data with a double-quote, tell Michael there is a problem'
  return '"{}"'.format('","'.join([p['name'], p['link'], p['photo_url'], p['country'], p['city'], p['zip'] ]))

csv_output = '"Name","Link","Photo","Country","City","Zip"\n{}'.format('\n'.join([to_row(p) for p in people]))

csv_file_path = path.expanduser("~/Downloads/{}.{}.csv".format(group_name, int(time.time())))
with open(csv_file_path, 'w') as csv_file:
  csv_file.write(csv_output)

print("Saved CSV to {}".format(csv_file_path))

call(['open', csv_file_path])

