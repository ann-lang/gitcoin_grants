import csv
#pk, month_index, intervention, time_after_intervention, num_commit, num_issue, num_star, num_comments, earning_after_adoption, count_grants, num_repos

info = dict()
file1 = open('RQ2/top500_month_commits.csv', 'r')
csv_reader = csv.reader(file1)
next(csv_reader)
for row in csv_reader:
	for i, num_commit in enumerate(row[1:]):
		index = i-6
		if index <= 0:
			intervention = 0
			time_after_intervention = 0
		else:
			intervention = 1
			time_after_intervention = index
		info[','.join([row[0], str(index)])] = [intervention, time_after_intervention, int(num_commit), 0, 0, 0, 0, 0, 0]
file1.close()

file2 = open('RQ2/top500_month_issues.csv', 'r')
csv_reader = csv.reader(file2)
next(csv_reader)
for row in csv_reader:
	for i, num_issue in enumerate(row[1:]):
		index = i-6
		info[','.join([row[0], str(index)])][3] = int(num_issue)
file2.close()

file3 = open('RQ2/top500_month_stars.csv', 'r')
csv_reader = csv.reader(file3)
next(csv_reader)
for row in csv_reader:
	for i, num_star in enumerate(row[1:]):
		index = i-6
		info[','.join([row[0], str(index)])][4] = int(num_star)
file3.close()

file4 = open('RQ2/top500_month_comments.csv', 'r')
csv_reader = csv.reader(file4)
next(csv_reader)
for row in csv_reader:
	for i, num_comment in enumerate(row[1:]):
		index = i-6
		info[','.join([row[0], str(index)])][5] = int(num_comment)
file4.close()

fund = dict()
repo = dict()
grants = dict()

file5 = open('RQ2/top500_fundings_withrepo.csv', 'r')
csv_reader = csv.reader(file5)
next(csv_reader)
for row in csv_reader:
	fund[row[0]] = float(row[1])
	repo[row[0]] = len(row[7].split(';'))
file5.close()


file6 = open('RQ1/grants.csv', 'r')
csv_reader = csv.reader(file6)
next(csv_reader)
for row in csv_reader:
	if row[4] not in grants.keys():
		grants[row[4]] = [row[0]]
	else:
		grants[row[4]].append(row[0])
file6.close()

for k in info:
	pk = k.split(',')[0]
	info[k][6] = fund[pk]
	info[k][7] = len(set(grants[pk]))
	info[k][8] = repo[pk]

#print(info)
file7 = open('info.csv', 'w')
csv_writer = csv.writer(file7)
csv_writer.writerow(['pk', 'month_index', 'intervention', 'time_after_intervention', 'num_commit', 'num_issue', 'num_star', 'num_comment', 'earning_after_adoption', 'count_grant', 'num_repo'])
for k in info.keys():
	pk = int(k.split(',')[0])
	month_index = int(k.split(',')[1])
	csv_writer.writerow([pk, month_index] + info[k])
file7.close()
