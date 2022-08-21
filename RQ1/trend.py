import csv
import requests
import json
from bs4 import BeautifulSoup

file = open('grants.csv', 'r')
csv_reader = csv.reader(file)
next(csv_reader)
d = dict()
#round_number,round_start_date,round_end_date,grant_title,grant_id,region,category,url,match_amount,num_contributions,num_unique_contributors,crowdfund_amount_contributions_usd,total
for row in csv_reader:
	try:
		match_amount = float(row[8][1:].strip().replace(',', ''))	
	except:
		match_amount = 0
	try:
		num_contributions = float(row[9].strip().replace(',', ''))
	except: 
		num_contributions = 0
	try:
		num_unique_contributors = float(row[10].strip().replace(',', ''))
	except:
		num_unique_contributors = 0
	try:
		crowdfund_amount_contributions_usd = float(row[11][1:].strip().replace(',', ''))
	except:
		crowdfund_amount_contributions_usd = 0
	try:
		total = float(row[12][1:].strip().replace(',', ''))
	except:
		total = 0
	pk = row[4]
	#type:[#grants, #total_funding]
	types = {'Community':[0,0], 'dApp Tech':[0,0], 'NFTs': [0,0], 'Infra Tech': [0,0],  
	'Grants Round 12': [0,0], 'Building Gitcoin': [0,0], 'dGov': [0,0], 'Health': [0,0], 'Crypto for Black Lives': [0,0], 'APOLLO': [0,0], 'Matic: Build-n-Earn': [0,0]}

	if row[0] not in d.keys():
		d[row[0]] = [1, match_amount,num_contributions,num_unique_contributors,crowdfund_amount_contributions_usd, total, [pk], types]
		types[row[6]][0] = 1
		types[row[6]][1] = total
	else:
		d[row[0]][0] += 1
		d[row[0]][1] += match_amount
		d[row[0]][2] += num_contributions
		d[row[0]][3] += num_unique_contributors
		d[row[0]][4] += crowdfund_amount_contributions_usd
		d[row[0]][5] += total
		d[row[0]][6].append(pk)
		d[row[0]][7][row[6]][0] += 1
		d[row[0]][7][row[6]][1] += total
file.close()

d = dict(sorted(d.items(), key=lambda item: int(item[0])))
pks = set()
for k in d.keys():
	num = 0
	for pk in d[k][6]:
		if pk not in pks:
			num += 1
			pks.add(pk)
		else:
			continue
	d[k].append(num)


file2 = open('trend.csv', 'w')
csv_writer = csv.writer(file2)
csv_writer.writerow(['#round_number', '#grants', 'match_amount', 'num_contributions', 'num_unique_contributors', 'crowdfund_amount_contributions_usd', 'total', '#new_projects'])
for k in d.keys():
	csv_writer.writerow([k]+d[k][0:6]+[d[k][8]])
file2.close()

file3 = open('trend_type_grants.csv', 'w')
csv_writer = csv.writer(file3)
csv_writer.writerow(['#round_number', 'type', '#grants'])
for k in d.keys():
	for type in d[k][7]:
		csv_writer.writerow([k]+[type]+[d[k][7][type][0]])
file3.close()

file4 = open('trend_type_total.csv', 'w')
csv_writer = csv.writer(file4)
csv_writer.writerow(['#round_number', 'type', 'total'])
for k in d.keys():
	for type in d[k][7]:
		csv_writer.writerow([k]+[type]+[d[k][7][type][1]])
file4.close()


