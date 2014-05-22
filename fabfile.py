# coding: utf-8
from fabric.api import env, local, cd, run
from fabric.colors import *
from fabric.operations import put

env.hosts = "www.ptphp.com"
env.user = "root"
env.usesshconfig = True
env.timeout = 20

def push():
    local('git add --all')
    local('git commit -m "deploy"')
    local('git push origin master')

