import csv
import matplotlib.pyplot as plt
import numpy as np 

def remove_outliers(data,threshold=3):
    mean_d = np.mean(data)
    std_d = np.std(data)
    data_ = []   
    for y in data:
        z_score= (y - mean_d)/std_d 
        if np.abs(z_score) <= threshold:
            data_.append(y)
    return data_

file1 = open('top500_month_stars.csv', 'r')
csv_reader = csv.reader(file1)
next(csv_reader)
stars = [[] for i in range(13)]
for row in csv_reader:
	for i in range(0,13):
		stars[i].append(int(row[i+1]))
file1.close()
"""
stars_ = []

for star in stars:
	star = remove_outliers(star,threshold=0.2)
	stars_.append(star)
print(len(stars_))
print(stars[12], stars_[12])
"""
labels = ['-6', '-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', '6']

fig, ax = plt.subplots()
#bplot = ax.boxplot(stars_, patch_artist=True, labels = labels)
#plt.yscale("log")
bplot = ax.boxplot(stars, patch_artist=True, showfliers=False, labels = labels)
colors = ['#929591', '#929591', '#929591', '#929591', '#929591', '#929591', 'green', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']

for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)
ax.set_xlabel('month index')
ax.set_ylabel('#star')
plt.savefig('stars.pdf')
#plt.show()

file1 = open('top500_month_commits.csv', 'r')
csv_reader = csv.reader(file1)
next(csv_reader)
commits = [[] for i in range(13)]
for row in csv_reader:
	for i in range(0,13):
		commits[i].append(int(row[i+1]))
file1.close()
"""
commits_ = []
for commit in commits:
	commit = remove_outliers(commit,threshold=0.2)
	commits_.append(commit)
print(len(commits_))
print(commits[12], commits_[12])
"""
labels = ['-6', '-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', '6']

fig, ax = plt.subplots()
bplot = ax.boxplot(commits, patch_artist=True, showfliers=False, labels = labels)
colors = ['#929591', '#929591', '#929591', '#929591', '#929591', '#929591', 'green', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']

for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)
ax.set_xlabel('month index')
ax.set_ylabel('#commit')
plt.savefig('commits.pdf')
#plt.show()



file1 = open('top500_month_issues.csv', 'r')
csv_reader = csv.reader(file1)
next(csv_reader)
issues = [[] for i in range(13)]
for row in csv_reader:
	for i in range(0,13):
		issues[i].append(int(row[i+1]))
file1.close()
"""
issues_ = []
for issue in issues:
	issue = remove_outliers(issue,threshold=0.2)
	issues_.append(issue)
print(len(issues_))
print(issues[12], issues_[12])
"""
labels = ['-6', '-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', '6']

fig, ax = plt.subplots()
bplot = ax.boxplot(issues, patch_artist=True, showfliers=False, labels = labels)
colors = ['#929591', '#929591', '#929591', '#929591', '#929591', '#929591', 'green', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']

for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)
ax.set_xlabel('month index')
ax.set_ylabel('#issue')
plt.savefig('issues.pdf')
#plt.show()


file1 = open('top500_month_comments.csv', 'r')
csv_reader = csv.reader(file1)
next(csv_reader)
comments = [[] for i in range(13)]
for row in csv_reader:
	for i in range(0,13):
		comments[i].append(int(row[i+1]))
file1.close()

"""
comments_ = []
for comment in comments:
	comment = remove_outliers(comment,threshold=0.2)
	comments_.append(comment)
print(len(comments_))
print(comments_[0])
"""
labels = ['-6', '-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', '6']

fig, ax = plt.subplots()
#plt.yscale("log")
bplot = ax.boxplot(comments, patch_artist=True, showfliers=False, labels = labels)
colors = ['#929591', '#929591', '#929591', '#929591', '#929591', '#929591', 'green', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']

for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)
ax.set_xlabel('month index')
ax.set_ylabel('#comment')
plt.savefig('comments.pdf')
#plt.show()