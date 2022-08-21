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
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


headers = {'Authorization': 'token %s' % ''}
file1 = open('top500_fundings.csv', 'r')
csv_reader = csv.reader(file1)
next(csv_reader)
info = dict()
#pk: totoal_funding, github_url(repo or org), main_page, category, grant_url, first_grant_date, repos
for row in csv_reader:
	if row[2]:
		info[row[0]] = [float(row[1])] + row[2:] + [datetime.strptime('2022/1/1', '%Y/%m/%d')]
file1.close()
print(len(info))
count_repo = 0
count_org = 0

file2 = open('RQ1/grants.csv', 'r')
csv_reader = csv.reader(file2)
next(csv_reader)
for row in csv_reader:
	date = datetime.strptime(row[1], '%Y/%m/%d')
	if row[4] in info.keys() and date < info[row[4]][5] and row[-1] and (float(row[-1][1:].strip().replace(',', ''))>0):
			info[row[4]][5] = date
file2.close()
"""
dd = datetime.strptime('2019/1/1', '%Y/%m/%d')
for k in info:
	if info[k][5] > dd:
		dd = info[k][5]
print(dd)
"""

def find_repo(github_url, first_grant_date):
	repos = []
	i = 1
	url = 'https://api.github.com/orgs/' + github_url[19:] + '/repos?page=%s&per_page=100'%(i)
	print(url)
	response = requests.get(url, headers=headers)
	response_dict = response.json()
	#print(response_dict)
	while len(response_dict) > 0:
		for repo in response_dict:
			#print(repo)
			if type(repo) is dict and repo['private'] is False and datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ') < (first_grant_date + relativedelta(months = 6, days = 15)) and datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ') > (first_grant_date - relativedelta(months = 6, days = 15)):
				repos.append(repo['html_url'])
			else:
				continue
		if len(response_dict) < 100:
			break
		i += 1
		url = 'https://api.github.com/orgs/' + github_url[19:] + '/repos?page=%s&per_page=100'%(i)
		print(url)
		
		response = requests.get(url, headers=headers)
		response_dict = response.json()
	#judge whether is a user account
	if len(repos) == 0:
		url = 'https://api.github.com/users/' + github_url[19:] + '/repos?page=%s&per_page=100'%(i)
		print(url)
		response = requests.get(url, headers=headers)
		response_dict = response.json()
		while len(response_dict) > 0:
			for repo in response_dict:
				#print(repo)
				if type(repo) is dict and repo['private'] is False and datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ') < (first_grant_date + relativedelta(months = 6, days = 15)) and datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ') > (first_grant_date - relativedelta(months = 6, days = 15)):
					repos.append(repo['html_url'])
				else:
					continue
			if len(response_dict) < 100:
				break
			i += 1
			url = 'https://api.github.com/users/' + github_url[19:] + '/repos?page=%s&per_page=100'%(i)
			print(url)
			
			response = requests.get(url, headers=headers)
			response_dict = response.json()
	return repos


num_repo = 0
for pk in info.keys():
	github_url = info[pk][1]
	if '/' in github_url[19:].strip('/'):
		tp = 'repo'
		count_repo += 1
	else:
		tp = 'org_user'
		count_org += 1
	if tp == 'repo':
		info[pk].append([github_url])
		num_repo += 1
	else:
		repos = find_repo(github_url, info[pk][5])
		print(repos)
		info[pk].append(repos)
		num_repo += len(repos)
print(count_org, count_repo)


file3 = open('top500_fundings_withrepo.csv', 'w')
csv_writer = csv.writer(file3)
csv_writer.writerow(['pk', 'totoal_funding', 'github_url', 'homepage', 'category', 'grant_url', 'first_grant_date', 'repos'])
for k in info.keys():
	#print(info[k])
	csv_writer.writerow([k]+[float(info[k][0])]+info[k][1:5]+[info[k][5].strftime("%Y/%m/%d %H:%M:%S")] + ["; ".join(str(x) for x in info[k][6])])
file3.close()
print('num_repos: %s'%num_repo)

