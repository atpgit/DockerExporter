import docker
import requests
import pypyodbc
import helperfor

# -*- coding: utf-8 -*-

class virtualhubs(object):
    """__init__() functions as the class constructor"""
    def __init__(self, name=None, HubId=None):
        self.name = name
        self.hubid = HubId

class ContainerMapping(object):
    """__init__() functions as the class constructor"""
    def __init__(self, name=None, HubId=None,ContainerId=None):
        self.ContainerId = ContainerId
        self.name = name
        self.hubid = HubId

client = docker.DockerClient(base_url='127.0.0.1:2375')
containers =client.containers.list()
for container in containers:
 print(container.name)
 print(container.id)
 print(container.status)
 
