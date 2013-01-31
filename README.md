# Gittime

Returns an estimation of the time spend coding based on commits in a git repository.

It supposes that developers commit regularly, at least once every 8 hours.
It considers only the master branch.
It does not take stashes in account.

Note: Please understand the limitations of this tool. It just gives an estimation, there is no guarantee of the accuracy.

## Requirements

	pip install -r requirements.txt
	
## Usage
	
	python gittime.py repo1 [repo2 ... repoN] [email1 ... emailN]
	
_repoX_ is a repository url (local or remote)

_emailX_ is used to filter by committer's email