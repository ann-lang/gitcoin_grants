import csv
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import time
from requests.auth import HTTPBasicAuth

times = dict()
file1 = open('RQ1/grants.csv', 'r')
csv_reader = csv.reader(file1)
next(csv_reader)
for row in csv_reader:
	if row[4] not in times.keys():
		times[row[4]] = [int(row[0])]
	else:
		times[row[4]].append(int(row[0]))
file1.close()


twitter_info = dict()
num_grants = 0
file2 = open('RQ3/twitter_accounts.csv', 'r')
csv_reader = csv.reader(file2)
next(csv_reader)

for row in csv_reader:
	grants = sorted(times[row[0]])
	num_grants += len(grants)
	twitter_info[row[0]] = [row[2], ';'.join([str(i) for i in grants])]
file2.close()

print(num_grants)

file3 = open('twitter_accounts_time.csv', 'w')
csv_writer = csv.writer(file3)
csv_writer.writerow(['pk', 'twitter', 'round_index'])
for k in twitter_info.keys():
	csv_writer.writerow([k]+twitter_info[k])

file3.close()
