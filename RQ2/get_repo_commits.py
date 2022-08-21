import csv
import requests
import json
import pandas as pd
import time
from requests.auth import HTTPBasicAuth
import re
import urllib
import urllib.request
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from tqdm import tqdm

hd_list = []

def obtain_commit(repo, start_date, end_date):
	i = 1
	idx = 0
	commits = []
	url = 'https://api.github.com/repos/' + repo[19:] + '/commits?since=%s&until=%s&page=%s&per_page=100'%(start_date, end_date, i)
	print(url)
	headers = {'Authorization': 'token %s' % hd_list[idx]}
	response = requests.get(url, headers=headers)
	limit = int(response.headers['x-RaTeLiMiT-lImIt'])
	if limit > 1:
		response_dict = response.json()
		#print(response_dict)
		while len(response_dict) > 0:
			for c in response_dict:
				#print(c)
				if type(c['author']) is dict and c['author']['type'] != 'Bot':
					commits.append([c['commit']['author']['name'],c['commit']['author']['date']])	
			if len(response_dict) < 100:
				break
			i += 1
			url = 'https://api.github.com/repos/' + repo[19:] + '/commits?since=%s&until=%s&page=%s&per_page=100'%(start_date, end_date, i)
			print(url)	
			headers = {'Authorization': 'token %s' % hd_list[idx]}
			response = requests.get(url, headers=headers)
			limit = int(response.headers['x-RaTeLiMiT-lImIt'])
			if limit > 1:
				response_dict = response.json()
			else:
				idx += 1
				if idx == len(hd_list):
					idx = 0
				headers = {'Authorization': 'token %s' % hd_list[idx]}
				response = requests.get(url, headers=headers)
				limit = int(response.headers['x-RaTeLiMiT-lImIt'])
				if limit > 1:
					response_dict = response.json()
				else:
					time_sleep = int(response.headers['x-ratelimit-reset'])-int(round(datetime.now().timestamp()))
					print(time_sleep)
					time.sleep(time_sleep+1)
					headers = {'Authorization': 'token %s' % hd_list[idx]}
					response = requests.get(url, headers=headers)
					response_dict = response.json()
	else:
		idx += 1
		if idx == len(hd_list):
			idx = 0
		headers = {'Authorization': 'token %s' % hd_list[idx]}
		response = requests.get(url, headers=headers)
		limit = int(response.headers['x-RaTeLiMiT-lImIt'])
		if limit > 1:
			response_dict = response.json()
		else:
			time_sleep = int(response.headers['x-ratelimit-reset'])-int(round(datetime.now().timestamp()))
			print(time_sleep)
			time.sleep(time_sleep+1)
			headers = {'Authorization': 'token %s' % hd_list[idx]}
			response = requests.get(url, headers=headers)
			response_dict = response.json()
		while len(response_dict) > 0:
			for c in response_dict:
				if type(c['author']) is dict and c['author']['type'] != 'Bot':
					commits.append([c['commit']['author']['name'],c['commit']['author']['date']])	
			if len(response_dict) < 100:
				break
			i += 1
			url = 'https://api.github.com/repos/' + repo[19:] + '/commits?since=%s&until=%s&page=%s&per_page=100'%(start_date, end_date, i)
			print(url)	
			headers = {'Authorization': 'token %s' % hd_list[idx]}
			response = requests.get(url, headers=headers)
			limit = int(response.headers['x-RaTeLiMiT-lImIt'])
			if limit > 1:
				response_dict = response.json()
			else:
				idx += 1
				if idx == len(hd_list):
					idx = 0
				headers = {'Authorization': 'token %s' % hd_list[idx]}
				response = requests.get(url, headers=headers)
				limit = int(response.headers['x-RaTeLiMiT-lImIt'])
				if limit > 1:
					response_dict = response.json()
				else:
					time_sleep = int(response.headers['x-ratelimit-reset'])-int(round(datetime.now().timestamp()))
					print(time_sleep)
					time.sleep(time_sleep+1)
					headers = {'Authorization': 'token %s' % hd_list[idx]}
					response = requests.get(url, headers=headers)
					response_dict = response.json()
	return commits


repo_commit = dict()
file1 = open('top500_fundings_withrepo.csv', 'r')
csv_reader = csv.reader(file1)
next(csv_reader)
#pk,totoal_funding,github_url,homepage,category,grant_url,first_grant_date,repos

row_num = 0
for row in tqdm(csv_reader):
	print('row_num: %s'%row_num)
	row_num += 1
	first_grant_date = datetime.strptime(row[6], "%Y/%m/%d %H:%M:%S")
	start_date = first_grant_date - relativedelta(months = 6, days = 15)
	start_date = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")

	end_date = first_grant_date + relativedelta(months = 6, days = 15)
	end_date = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
	repos = row[7].split(';')
	for repo in repos:
		repo = repo.strip()
		try:
			commits = obtain_commit(repo, start_date, end_date)
			print('len_commits: %s'%len(commits))
			if row[0] not in repo_commit:
				repo_commit[row[0]] = commits
			else:
				repo_commit[row[0]] += commits
		except:
			repo_commit[row[0]] = []
file1.close()

file2 = open('top500_commits.csv', 'w')
csv_writer = csv.writer(file2)
csv_writer.writerow(['pk', 'commits'])
for k in repo_commit:
	commits_ = []
	commits = repo_commit[k]
	for c in commits:
		commits_.append(c[0]+':'+c[1])

	csv_writer.writerow([k, ';'.join(item for item in commits_)])
file2.close()
	

