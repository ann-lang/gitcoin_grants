import csv
import requests
import json
#from bs4 import BeautifulSoup
import pandas as pd
import time
from requests.auth import HTTPBasicAuth


file = open('grants.csv', 'r')
csv_reader = csv.reader(file)
next(csv_reader)
pks = set()
#round_number,round_start_date,round_end_date,grant_title,grant_id,region,category,url,match_amount,num_contributions,num_unique_contributors,crowdfund_amount_contributions_usd,total
for row in csv_reader:
	pks.add(row[4])
file.close()
print(len(pks))

file1 = open('all_info_grants.csv', 'w')
csv_writer = csv.writer(file1)
csv_writer.writerow(['id', 'slug', 'description', 'reference_url', 'admin_profile_followers', 'admin_profile_following', 'admin_position', 
	'admin_grants_owned', 'admin_grants_contributed', 'admin_github_url', 'num_team_member'])
for pk in pks:
	url = "https://gitcoin.co/api/v0.1/grants/?pk=%s"%(pk)
	print(url)
	try:
		r = requests.get(url)
		input = r.json()[0]
		if 'followers' in input['admin_profile'].keys():
			followers = int(input['admin_profile']['followers']) 
		else:
			followers = -1
		if 'following' in input['admin_profile'].keys():
			following = int(input['admin_profile']['following']) 
		else:
			following = -1
		if 'position' in input['admin_profile'].keys():
			position = int(input['admin_profile']['position']) 
		else:
			position = -1
		if 'grants_owned' in input['admin_profile'].keys():
			grants_owned = int(input['admin_profile']['grants_owned']) 
		else:
			grants_owned = -1
		if 'grants_contributed' in input['admin_profile'].keys():
			grants_contributed = int(input['admin_profile']['grants_contributed']) 
		else:
			grants_contributed = -1
		if 'github_url' in input['admin_profile'].keys():
			github_url = input['admin_profile']['github_url']
		else:
			github_url = ''
		csv_writer.writerow([int(input['id']), input['slug'], input['description'], input['reference_url'], followers, following, position, grants_owned, grants_contributed, github_url, int(len(input['team_members']))])
		time.sleep(1)
	except:
		print(pk)


file1.close()