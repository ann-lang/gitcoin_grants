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

def obtain_commits_comments(repo, start_date, end_date):
	i = 1
	idx = 0
	commit_comments = []
	url = 'https://api.github.com/repos/' + repo[19:] + '/comments?&page=%s&per_page=100'%(i)
	print(url)
	headers = {'Authorization': 'token %s' % hd_list[idx]}
	response = requests.get(url, headers=headers)
	limit = int(response.headers['x-RaTeLiMiT-lImIt'])
	if limit > 1:
		response_dict = response.json()
		#print(response_dict)
		while len(response_dict) > 0:
			flag = False
			for c in response_dict:
				#print(c)
				created_at = datetime.strptime(c['created_at'], "%Y-%m-%dT%H:%M:%SZ")
				if created_at < datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%SZ") and created_at > datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ"):
					commit_comments.append(created_at.strftime("%Y-%m-%dT%H:%M:%SZ"))
					#print(commit_comments)
				elif created_at >= datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%SZ"):
					flag = True
					break
			if flag:
				break					
			if len(response_dict) < 100:
				break
			i += 1
			url = 'https://api.github.com/repos/' + repo[19:] + '/comments?page=%s&per_page=100'%(i)
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
			flag = False
			for c in response_dict:
				created_at = datetime.strptime(c['created_at'], "%Y-%m-%dT%H:%M:%SZ")
				if created_at < datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%SZ") and created_at > datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ"):
					commit_comments.append(created_at.strftime("%Y-%m-%dT%H:%M:%SZ"))
					#print(commit_comments)
				elif created_at >= datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%SZ"):
					flag = True
					break
			if flag:
				break
			if len(response_dict) < 100:
				break
			i += 1
			url = 'https://api.github.com/repos/' + repo[19:] + '/comments?page=%s&per_page=100'%(i)
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
	return commit_comments


repo_commit_comments = dict()
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
			commit_comments = obtain_commits_comments(repo, start_date, end_date)
			print('len_commit_comments: %s'%len(commit_comments))
			if row[0] not in repo_commit_comments:
				repo_commit_comments[row[0]] = commit_comments
			else:
				repo_commit_comments[row[0]] += commit_comments
		except:
			repo_commit_comments[row[0]] = []
file1.close()

file2 = open('top500_commit_comments.csv', 'w')
csv_writer = csv.writer(file2)
csv_writer.writerow(['pk', 'commit_comments'])
for k in repo_commit_comments:
	csv_writer.writerow([k, ';'.join(item for item in repo_commit_comments[k])])
file2.close()

