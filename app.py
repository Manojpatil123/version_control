import git      #pip install gitpython
g = git.cmd.Git()
blob = g.ls_remote('https://github.com/Manojpatil123/version_control.git', sort='-v:refname', tags=True)
tags=blob.split('\n')[0].split('/')[-1]
print(tags)

from version import get_version

version=get_version()