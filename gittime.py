#!/usr/bin/env python

import signal, os, shutil, os, sys, re
from git import Repo

directory = False


def get_repo(repo_path, branch):	
	global directory
	if (repo_path.startswith("git@") or repo_path.startswith("http")):
		directory = 'repo'
		if os.path.exists(directory):
			sys.exit('Cannot clone in "%s": directory exists' % directory)
		else:
			os.makedirs(directory)
		
		repo = Repo.init(directory)
		remote = repo.create_remote('origin', repo_path)
		remote.pull(branch)	
	else:
		repo = Repo(repo_path)	
		
	return repo	


def clean_repo():
	if directory and os.path.exists(directory):
		shutil.rmtree(directory)


def get_commits_time_intervals(repo, branch, committers=[]):
	commit_dates = sorted([commit.committed_date for commit in repo.iter_commits(branch) if not committers or commit.committer.email in committers])
	commits_time_intervals = []
	for index in range(1,len(commit_dates)):
		interval = commit_dates[index] - commit_dates[index-1]
		commits_time_intervals.append(interval)
	return commits_time_intervals


def get_commits_time(repo_path, branch="master", committers=[], hours_thresh = 8*60*60):
	repo = get_repo(repo_path, branch)
	commits_time_intervals = get_commits_time_intervals(repo, branch, committers)
	clean_repo()
	return sum([time_interval for time_interval in commits_time_intervals if (time_interval < hours_thresh)])


""" not used
def cluster(datalist):
	from numpy import array
	from scipy.cluster.vq import kmeans2, vq, whiten

	data = array(datalist)
	
	centroids,_ = kmeans2(data, 3, minit="points")
	idx,_ = vq(data,centroids)
	
	print ['%.3f'%(val/60.0/60) for val in centroids]
	
	print ['%.3f'%(val/60.0/60) for val in data[idx==0]]
	print ['%.3f'%(val/60.0/60) for val in data[idx==1]]
	print ['%.3f'%(val/60.0/60) for val in data[idx==2]]
	print ['%.3f'%(val/60.0/60) for val in data[idx==3]]
"""


def handler(signum, frame):
	clean_repo()


def main():
	signal.signal(signal.SIGTERM, handler)
	signal.signal(signal.SIGINT, handler)

	committers = []
	repos = []
	
	for arg in sys.argv[1:]:
		if re.search("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}", arg):
			committers.append(arg)
		else:
			repos.append(arg)
	
	if not repos:
		print 'usage: gittime.py repo1 [repo2 ... repoN] [email1 ... emailN]'
		sys.exit(0)
	
	time = 0
	for repo in repos:
		repo_time = get_commits_time(repo, committers=committers)
		print "%s: %s" % (os.path.basename(repo.strip("/")), round(repo_time/60.0/60, 1))
		time += repo_time
	
	print "total: %s hours" % round(time/60.0/60, 1)


if __name__ == "__main__":
	main()