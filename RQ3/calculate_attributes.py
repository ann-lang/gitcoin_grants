import csv
import requests
import json
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import sys
csv.field_size_limit(sys.maxsize)

attri = dict() #'pk: round: total_earned, category, #round_times, #team_member, len_description, 
#admin_profile_followers, admin_profile_following, admin_position, admin_grants_owned, admin_grants_contributed
##stars, #commits, #issues, #comments
#tweet_count,count_likes,count_comments,count_retweet
#followers_count,followings_count


times = dict()
pks = []
round_ = dict()

file0 = open('RQ2/top500_fundings_withrepo.csv', 'r')
csv_reader = csv.reader(file0)
next(csv_reader)
for row in csv_reader:
	pks.append(row[0])
file0.close()

file1 = open('RQ1/grants.csv', 'r')
csv_reader = csv.reader(file1)
next(csv_reader)
for row in csv_reader:
	if row[4] in pks:
		pk = row[4]
		round_id = row[0]
		start_date = row[1]
		end_date = row[2]
		try:
			total = float(row[-1][1:].replace(',', ''))
		except:
			total = 0
		if pk not in attri.keys():
			attri[pk] = {round_id: [total, row[6]]}
		else:
			attri[pk][round_id] = [total, row[6]]

		if pk not in times.keys():
			times[pk] = [int(round_id)]
		else:
			times[pk].append(int(round_id))
		if round_id not in round_.keys():
			round_[round_id] = [start_date, end_date]
file1.close()

for k in times:
	times[k].sort()
#print(attri)
#print(times)

for pk in attri.keys():
	for round_id in attri[pk].keys():
		round_times = times[pk].index(int(round_id)) + 1
		#print(times[pk], round_id, round_times)
		attri[pk][round_id].append(round_times)
num_grants = 0
for k in attri.keys():
	num_grants += len(attri[k])
print(num_grants) #770
print(len(attri))
#print(attri)


file2 = open('RQ1/all_info_grants.csv', 'r')
csv_reader = csv.reader(file2)
next(csv_reader)
for row in csv_reader:
	team_member = int(row[-1])
	len_description = len(row[2])
	admin_profile_followers = int(row[4])
	admin_profile_following = int(row[5])
	admin_position = int(row[6]) 
	admin_grants_owned = int(row[7])
	admin_grants_contributed = int(row[8])
	if row[0] in attri.keys():
		for round_id in attri[row[0]]:
			attri[row[0]][round_id] += [team_member, len_description, admin_profile_followers,admin_profile_following,admin_position,admin_grants_owned,admin_grants_contributed]
file2.close()
#print(attri)
for pk in attri:
	for round_id in attri[pk]:
		if len(attri[pk][round_id]) == 3:
			attri[pk][round_id] += [-1, -1, -1, -1, -1, -1, -1]

repo_stars = dict()
file3 = open('RQ2/top500_stars.csv', 'r')
csv_reader = csv.reader(file3)
next(csv_reader)
for row in csv_reader:
	k = row[0]
	star_dates_str = row[1].split(';')
	star_dates = []
	for item in star_dates_str:
		#print(item)
		try:
			item = datetime.strptime(item, "%Y-%m-%dT%H:%M:%SZ")
			star_dates.append(item)
		except:
			continue
	star_dates.sort()
	repo_stars[k] = star_dates
file3.close()

for pk in attri.keys():
	for round_id in attri[pk]:
		start_date = datetime.strptime(round_[round_id][0], "%Y/%m/%d")
		end_date = datetime.strptime(round_[round_id][1], "%Y/%m/%d")
		num_star = 0
		for time in repo_stars[pk]:
			if time >= start_date and time <= end_date:
				num_star += 1
		attri[pk][round_id].append(num_star)
		#print(num_star)

repo_commits = dict()
file4 = open('RQ2/top500_commits.csv', 'r')
csv_reader = csv.reader(file4)
next(csv_reader)
for row in csv_reader:
	k = row[0]
	author_commits = row[1].split(';')
	commit_dates = []
	for item in author_commits:
		#print(item)
		try:
			item = item[item.index(':')+1:]
			#print(item)
			item = datetime.strptime(item, "%Y-%m-%dT%H:%M:%SZ")
			commit_dates.append(item)
		except:
			continue
	commit_dates.sort()
	repo_commits[k] = commit_dates
file4.close()

for pk in attri.keys():
	for round_id in attri[pk]:
		start_date = datetime.strptime(round_[round_id][0], "%Y/%m/%d")
		end_date = datetime.strptime(round_[round_id][1], "%Y/%m/%d")
		num_commits = 0
		for time in repo_commits[pk]:
			if time >= start_date and time <= end_date:
				num_commits += 1
		attri[pk][round_id].append(num_commits)
		#print(num_commits)

repo_issues = dict()
file5 = open('RQ2/top500_issues.csv', 'r')
csv_reader = csv.reader(file5)
next(csv_reader)
for row in csv_reader:
	k = row[0]
	issue_dates_str = row[1].split(';')
	issue_dates = []
	for item in issue_dates_str:
		#print(item)
		try:
			item = datetime.strptime(item, "%Y-%m-%dT%H:%M:%SZ")
			issue_dates.append(item)
		except:
			continue
	issue_dates.sort()
	repo_issues[k] = issue_dates
file5.close()

for pk in attri.keys():
	for round_id in attri[pk]:
		start_date = datetime.strptime(round_[round_id][0], "%Y/%m/%d")
		end_date = datetime.strptime(round_[round_id][1], "%Y/%m/%d")
		num_issues = 0
		for time in repo_issues[pk]:
			if time >= start_date and time <= end_date:
				num_issues += 1
		attri[pk][round_id].append(num_issues)
		#print(num_issues)

repo_comments = dict()
repo_comments_str = dict()
file6 = open('RQ2/top500_issue_comments.csv', 'r')
csv_reader = csv.reader(file6)
next(csv_reader)
for row in csv_reader:
	k = row[0]
	repo_comments_str[k] = row[1].split(';')
file6.close()
	
file7 = open('RQ2/top500_commit_comments.csv', 'r')
csv_reader = csv.reader(file7)
next(csv_reader)
for row in csv_reader:
	k = row[0]
	repo_comments_str[k] += row[1].split(';')
file7.close()

file8 = open('RQ2/top500_pr_comments.csv', 'r')
csv_reader = csv.reader(file8)
next(csv_reader)
for row in csv_reader:
	k = row[0]
	repo_comments_str[k] += row[1].split(';')
file8.close()


for k in repo_comments_str.keys():
	comment_dates = []
	for item in repo_comments_str[k]:
		#print(item)
		try:
			item = datetime.strptime(item, "%Y-%m-%dT%H:%M:%SZ")
			comment_dates.append(item)
		except:
			continue
	comment_dates.sort()
	repo_comments[k] = comment_dates

for pk in attri.keys():
	for round_id in attri[pk]:
		start_date = datetime.strptime(round_[round_id][0], "%Y/%m/%d")
		end_date = datetime.strptime(round_[round_id][1], "%Y/%m/%d")
		num_comments = 0
		for time in repo_comments[pk]:
			if time >= start_date and time <= end_date:
				num_comments += 1
		attri[pk][round_id].append(num_comments)
		#print(num_comments)

file9 = open('RQ3/twitter/tweet_statistic.csv', 'r')
csv_reader = csv.reader(file9)
next(csv_reader)
for row in csv_reader:
	pk = row[0]
	round_index = row[2]
	#print([int(i) for i in row[3:]])
	attri[pk][round_index] += [int(i) for i in row[3:]]
file9.close()

for pk in attri:
	for round_id in attri[pk]:
		#print(len(attri[pk][round_id]))
		if len(attri[pk][round_id]) != 18:
			attri[pk][round_id] += [-1, -1, -1, -1]
#print(attri)

file10 = open('RQ3/twitter/follower_following.csv', 'r')
csv_reader = csv.reader(file10)
next(csv_reader)
for row in csv_reader:
	pk = row[0]
	for round_id in attri[pk].keys():
		attri[pk][round_id] += [int(row[3]), int(row[4])]
file10.close()


for pk in attri:
	for round_id in attri[pk]:
		#print(len(attri[pk][round_id]))
		if len(attri[pk][round_id]) != 20:
			attri[pk][round_id] += [-1, -1]


for k in attri.keys():
	for kk in attri[k]:
		if len(attri[k][kk]) != 20:
			print(len(attri[k][kk]))


file11 = open('grant_attri.csv', 'w')
csv_writer = csv.writer(file11)
csv_writer.writerow(['pk', 'round', 'total_earned', 'category', 'round_times', 'team_member', 'len_description', 'admin_profile_followers', 'admin_profile_following', 'admin_position', 'admin_grants_owned', 'admin_grants_contributed', 'stars', 'commits', 'issues', 'comments', 'tweet_count', 'count_likes', 'count_comments', 'count_retweet', 'followers_count', 'followings_count'])
for pk in attri:
	for round_id in attri[pk]:
		att = attri[pk][round_id]
		for i in range(len(att)):
			if att[i] == -1:
				att[i] = ''
		csv_writer.writerow([pk, round_id] + att)
file11.close()


file12 = open('project_attri.csv', 'w')
csv_writer = csv.writer(file12)

csv_writer.writerow(['pk', 'total_earned', 'category', 'num_round', 'team_member', 'len_description', 'admin_profile_followers', 'admin_profile_following', 'admin_position', 'admin_grants_owned', 'admin_grants_contributed', 'stars', 'commits', 'issues', 'comments', 'tweet_count', 'count_likes', 'count_comments', 'count_retweet', 'followers_count', 'followings_count'])
for pk in attri:
	total_earned = None
	category = None
	num_round = len(attri[pk])
	team_member, len_description = [], []
	admin_profile_followers, admin_profile_following, admin_position, admin_grants_owned, admin_grants_contributed = [], [], [], [], []
	stars, commits, issues, comments = None, None, None, None
	tweet_count, count_likes, count_comments, count_retweet, followers_count, followings_count = None, None, None, None, None, None

	for round_id in attri[pk]:
		att = attri[pk][round_id]
		total_earned = att[0] if not total_earned else total_earned + att[0]
		if not category: category = att[1]
		team_member.append(att[3])
		len_description.append(att[4])
		admin_profile_followers.append(att[5])
		admin_profile_following.append(att[6])
		admin_position.append(att[7])
		admin_grants_owned.append(att[8])
		admin_grants_contributed.append(att[9])
		stars = att[10] if not stars else stars + att[10]
		commits = att[11] if not commits else commits + att[11]
		issues = att[12] if not issues else issues + att[12]
		comments = att[13] if not comments else comments + att[13]
		tweet_count = att[14] if not tweet_count else tweet_count + att[14]
		count_likes = att[15] if not count_likes else count_likes + att[15]
		count_comments = att[16] if not count_comments else count_comments + att[16]
		count_retweet = att[17] if not count_retweet else count_retweet + att[17]
		if not followers_count: followers_count = att[18]
		if not followings_count: followings_count = att[19]

	try:
		team_member = np.median(team_member)
	except:
		team_member = None
	try:
		len_description = np.median(len_description)
	except:
		len_description = None
	try:
		admin_profile_followers = np.median(admin_profile_followers)
	except:
		admin_profile_followers = None
	try:
		admin_profile_following = np.median(admin_profile_following)
	except:
		admin_profile_following = None
	try:
		admin_position = np.median(admin_position)
	except:
		admin_position = None
	try:
		admin_grants_owned = np.median(admin_grants_owned)
	except:
		admin_grants_owned = None
	try:
		admin_grants_contributed = np.median(admin_grants_contributed)
	except:
		admin_grants_contributed = None
	res = [pk, total_earned, category, num_round, team_member, len_description, admin_profile_followers, admin_profile_following, admin_position, admin_grants_owned, admin_grants_contributed, stars, commits, issues, comments, tweet_count, count_likes, count_comments, count_retweet, followers_count, followings_count]
	for i in range(len(res)):
		if res[i] == -1:
			res = ''
	csv_writer.writerow(res)
file11.close()










