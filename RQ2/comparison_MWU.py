import csv
from scipy.stats import mannwhitneyu
import numpy as np
from scipy.stats import norm

def mann(before, after):
	U1, p = mannwhitneyu(before, after)
	n_before, n_after = len(before), len(after)
	U2 = n_before*n_after - U1
	U = min(U1, U2)
	N = n_before + n_after
	z = (U - n_before*n_after/2 + 0.5) / np.sqrt(n_before*n_after * (N + 1)/ 12)
	r = np.abs(z/np.sqrt(N))
	return U1, p, r


file1 = open('top500_month_stars.csv', 'r')
csv_reader = csv.reader(file1)
next(csv_reader)

results = dict() #pk: 1: small effect size, 2: med effect size, 3: large effect size, 0: less than small effect size
# *: no sig differences, -1: cannnot comparsion [star, comments, commits]
stars = dict()
for row in csv_reader:
	stars[row[0]] = [[int(i) for i in row[1:7]], [int(i) for i in row[8:14]]]
file1.close()

diff = 0
non_diff = 0
for k in stars:
	before = stars[k][0]
	after = stars[k][1]
	try:
		U1, p, r = mann(before, after) 
		if p < 0.05:
			diff += 1
			if r >= 0.5:
				results[k] = [before, after, 3]
			elif r >= 0.3:
				results[k] = [before, after, 2]
			elif r >= 0.1:
				results[k] = [before, after, 1]
			else:
				results[k] = [before, after, 0]
		else:
			non_diff += 1
			results[k] = [before, after, '*']
	except:
		results[k] = [before, after, -1]
		continue
print(diff, non_diff)


file2 = open('top500_month_comments.csv', 'r')
csv_reader = csv.reader(file2)
next(csv_reader)

comments = dict()
for row in csv_reader:
	comments[row[0]] = [[int(i) for i in row[1:7]], [int(i) for i in row[8:14]]]
file1.close()

diff = 0
non_diff = 0
for k in comments:
	before = comments[k][0]
	after = comments[k][1]
	try:
		U1, p, r = mann(before, after) 
		if p < 0.05:
			diff += 1
			if r >= 0.5:
				results[k].append([before, after, 3])
			elif r >= 0.3:
				results[k].append([before, after, 2])
			elif r >= 0.1:
				results[k].append([before, after, 1])
			else:
				results[k].append([before, after, 0])
		else:
			non_diff += 1
			results[k].append([before, after, '*'])
	except:
		results[k].append([before, after, -1])
		continue
print(diff, non_diff)


file2 = open('top500_month_commits.csv', 'r')
csv_reader = csv.reader(file2)
next(csv_reader)

commits = dict()
for row in csv_reader:
	commits[row[0]] = [[int(i) for i in row[1:7]], [int(i) for i in row[8:14]]]
file1.close()

diff = 0
non_diff = 0
for k in commits:
	before = commits[k][0]
	after = commits[k][1]
	try:
		U1, p, r = mann(before, after) 
		if p < 0.05:
			diff += 1
			if r >= 0.5:
				results[k].append([before, after, 3])
			elif r >= 0.3:
				results[k].append([before, after, 2])
			elif r >= 0.1:
				results[k].append([before, after, 1])
			else:
				results[k].append([before, after, 0])
		else:
			non_diff += 1
			results[k].append([before, after, '*'])
	except:
		results[k].append([before, after, -1])
		continue
print(diff, non_diff)

print(len(results))
for k in results.keys():
	print(k, results[k])