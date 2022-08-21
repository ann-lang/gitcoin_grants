import csv
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import sys

csv.field_size_limit(sys.maxsize)


repo_grant_date = dict()
file1 = open('top500_fundings_withrepo.csv', 'r')
csv_reader = csv.reader(file1)
next(csv_reader)
#pk,totoal_funding,github_url,homepage,category,grant_url,first_grant_date,repos

for row in csv_reader:
	first_grant_date = datetime.strptime(row[6], "%Y/%m/%d %H:%M:%S")
	#start_date = first_grant_date - relativedelta(months = 6, days = 15)
	#start_date = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")

	#end_date = first_grant_date + relativedelta(months = 6, days = 15)
	#end_date = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
	if row[0] not in repo_grant_date.keys():
		repo_grant_date[row[0]] = first_grant_date
file1.close()
		

repo_commits = dict()

file2 = open('top500_commits.csv', 'r')
csv_reader = csv.reader(file2)
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
	#print(commit_dates)
	i = 0
	start_date = repo_grant_date[k] - relativedelta(months = 6, days = 15)
	end_date = repo_grant_date[k] + relativedelta(months = 6, days = 15)
	date = start_date + relativedelta(months = 1)
	num = 0
	repo_commits[k] = [0 for i in range(13)]
	index = 0
	if len(commit_dates) > 0:
		while i < len(commit_dates) and commit_dates[i] < start_date:
			i += 1
		while i < len(commit_dates):
			if commit_dates[i] > end_date:
				break
			elif commit_dates[i] < date and commit_dates[i] >= start_date:
				num += 1
				i += 1
			else:
				repo_commits[k][index] += num
				num = 0
				index += 1
				start_date = date
				date += relativedelta(months = 1)
		if index < 13:
			repo_commits[k][index] += num

file3 = open('top500_month_commits.csv', 'w')
csv_writer = csv.writer(file3)
csv_writer.writerow(['pk', '-6', '-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', '6'])
for pk in repo_commits.keys():		
	csv_writer.writerow([pk]+repo_commits[pk])
file3.close()


repo_issues = dict()
file4 = open('top500_issues.csv', 'r')
csv_reader = csv.reader(file4)
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
	#print(commit_dates)
	i = 0
	start_date = repo_grant_date[k] - relativedelta(months = 6, days = 15)
	end_date = repo_grant_date[k] + relativedelta(months = 6, days = 15)
	date = start_date + relativedelta(months = 1)
	#print(start_date, issue_dates[-1])
	num = 0
	#print(len(issue_dates))
	repo_issues[k] = [0 for i in range(13)]
	index = 0
	if len(issue_dates) > 0:
		while i < len(issue_dates) and issue_dates[i] < start_date:
			i += 1
		while i < len(issue_dates):
			if issue_dates[i] > end_date:
				break
			elif issue_dates[i] < date and issue_dates[i] >= start_date:
				num += 1
				i += 1
			else:
				repo_issues[k][index] += num
				num = 0
				index += 1
				start_date = date
				date += relativedelta(months = 1)
		if index < 13:
			repo_issues[k][index] += num

file5 = open('top500_month_issues.csv', 'w')
csv_writer = csv.writer(file5)
csv_writer.writerow(['pk', '-6', '-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', '6'])
for pk in repo_issues.keys():		
	csv_writer.writerow([pk]+repo_issues[pk])
file5.close()



repo_comments = dict()
repo_comments_str = dict()
file6 = open('top500_issue_comments.csv', 'r')
csv_reader = csv.reader(file6)
next(csv_reader)
for row in csv_reader:
	k = row[0]
	repo_comments_str[k] = row[1].split(';')
file6.close()
	
file7 = open('top500_commit_comments.csv', 'r')
csv_reader = csv.reader(file7)
next(csv_reader)
for row in csv_reader:
	k = row[0]
	repo_comments_str[k] += row[1].split(';')
file7.close()

file8 = open('top500_pr_comments.csv', 'r')
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
	#print(commit_dates)
	i = 0
	start_date = repo_grant_date[k] - relativedelta(months = 6, days = 15)
	end_date = repo_grant_date[k] + relativedelta(months = 6, days = 15)
	date = start_date + relativedelta(months = 1)
	num = 0
	#print(len(issue_dates))
	repo_comments[k] = [0 for i in range(13)]
	index = 0
	if len(comment_dates) > 0:
		while i < len(comment_dates) and  comment_dates[i] < start_date:
			i += 1
		while i < len(comment_dates):
			if comment_dates[i] > end_date:
				break
			elif comment_dates[i] < date and comment_dates[i] >= start_date:
				num += 1
				i += 1
			else:
				repo_comments[k][index] += num
				num = 0
				index += 1
				start_date = date
				date += relativedelta(months = 1)
		if index < 13:
			repo_comments[k][index] += num


file9 = open('top500_month_comments.csv', 'w')
csv_writer = csv.writer(file9)
csv_writer.writerow(['pk', '-6', '-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', '6'])
for pk in repo_comments.keys():		
	csv_writer.writerow([pk]+repo_comments[pk])
file9.close()


repo_stars = dict()
file10 = open('top500_stars.csv', 'r')
csv_reader = csv.reader(file10)
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
	#print(commit_dates)
	i = 0
	start_date = repo_grant_date[k] - relativedelta(months = 6, days = 15)
	end_date = repo_grant_date[k] + relativedelta(months = 6, days = 15)
	date = start_date + relativedelta(months = 1)
	#print(start_date, issue_dates[-1])
	num = 0
	#print(len(issue_dates))
	repo_stars[k] = [0 for i in range(13)]
	index = 0
	if len(star_dates) > 0:
		while i < len(star_dates) and star_dates[i] < start_date:
			i += 1
		while i < len(star_dates):
			if star_dates[i] > end_date:
				break
			elif star_dates[i] < date and star_dates[i] >= start_date:
				num += 1
				i += 1
			else:
				repo_stars[k][index] += num
				num = 0
				index += 1
				start_date = date
				date += relativedelta(months = 1)
		if index < 13:
			repo_stars[k][index] += num

file11 = open('top500_month_stars.csv', 'w')
csv_writer = csv.writer(file11)
csv_writer.writerow(['pk', '-6', '-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', '6'])
for pk in repo_stars.keys():		
	csv_writer.writerow([pk]+repo_stars[pk])
file11.close()