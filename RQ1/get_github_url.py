import csv
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import time
from requests.auth import HTTPBasicAuth
import re
import urllib
import urllib.request


def get_url(description):
	url = re.findall('https?://github.com/[-A-Za-z0-9+&@#%?=~_|!:,.;]+[/]{0,1}[-A-Za-z0-9+&@#%?=~_|!:,.;]+', description)
	return url


file = open('all_info_grants.csv', 'r')
csv_reader = csv.reader(file)
next(csv_reader)
d = dict()
num = 0
#'id', 'slug', 'description', 'reference_url', 'admin_profile_followers', 'admin_profile_following', 'admin_position', 'admin_grants_owned', 'admin_grants_contributed', 'admin_github_url', 'num_team_member'
for row in csv_reader:
	print(num)
	num += 1
	url = row[3]
	if url.startswith('https://github.com/'):
		d[row[0]] = url
	else:
		url = get_url(row[2])
		if url:
			print('description: ', row[0], url)
			d[row[0]] = url
		else:
			try:
				mainpage_url = row[3]
				print(mainpage_url)
				with urllib.request.urlopen(mainpage_url, timeout=5) as url:
					s = url.read()
					soup = BeautifulSoup(s, "html.parser")
					all_tag_a = soup.find_all("a", limit=10)
					for links in all_tag_a:
						href = links.get('href')
						url = get_url(href)
						if url:
							print('mainpage: ', row[0], url)
							if row[0] not in d.keys():
								d[row[0]] = url
							else:
								d[row[0]] += url
						else:
							continue
			except:
				continue
file.close()

file = open('github_url.csv', 'w')
csv_writer = csv.writer(file)
csv_writer.writerow(['pk', 'github_url'])
for k in d:
	csv_writer.writerow([k, d[k]])
file.close()