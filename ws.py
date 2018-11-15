import cherrypy
import pandas as pd
import docker
import myprocessor
import exportermodel
import os
p = myprocessor.MyProcessor()


class MyWebService(object):
  
   @cherrypy.expose
   def metrics(self):
      client = docker.DockerClient(base_url='127.0.0.1:2375')
      containers =client.containers.list()
      THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
      my_file = os.path.join(THIS_FOLDER, 'copy.txt')
      my_file = open("copy.txt", "w") 
      my_file.writelines("#Helper Docker Exporter Started\n")
      my_file = open("copy.txt", "a") 
      my_file.writelines("containers_total_count ")
      my_file.writelines(str(len(containers)))
      my_file.writelines("\n") 
  

      my_file = open("copy.txt", "r") #test
      fileData = my_file.readlines()
      my_file.close() 
      return fileData
if __name__ == '__main__':
  config = {'server.socket_host': '127.0.0.1','server.socket_port':8585}
  cherrypy.response.headers['Content-Type'] = 'text/plain'
  cherrypy.config.update(config)
  cherrypy.quickstart(MyWebService())