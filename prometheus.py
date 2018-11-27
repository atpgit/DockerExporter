from prometheus_client import start_http_server, Summary, Counter, Metric, Gauge, Info, make_wsgi_app
import time
import docker
import json
# from flask import Flask
# from werkzeug.wsgi import DispatcherMiddleware

def get_Dict_Value(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return dictionary[key]
    raise IndexError("dictionary index out of range") 

def bytesToMB(value):
    return value / 1000 / 1000

def jsonDefault(object):
    return object.__dict__

#con.stats.cpu,con.stats.memory,con.stats.ioWrite, con.stats.ioRead,con.stats.networkSend,con.stats.networkReceive
def toJSON(con):
    return {
        'id' : con.id,
        'name' : con.name,
        'status' : con.status,
        'cpu' : str(con.cpu),
        'memory' : str(con.memory),
        'ioWrite' : str(con.ioWrite),
        'ioRead' : str(con.ioRead),
        'networkSend' : str(con.networkSend),
        'networkReceive' : str(con.networkReceive)
    }

# class list:
#     def toJSON(self):
#         return json.dumps(self, default=lambda o: o.__dict__, 
#             sort_keys=True, indent=4)

class Container() :
    def __init__(self,id,name,status,cpu,memory,ioWrite,ioRead,networkReceive,networkSend) :
        self.id= id
        self.name= name
        self.status = status
        self.cpu= cpu
        self.memory= memory
        self.ioWrite = ioWrite
        self.ioRead = ioRead
        self.networkReceive = networkReceive
        self.networkSend = networkSend

c = Counter('docker_container', 'Container List', ['Id', 'Name', 'Status', "Cpu", "Memory", "IOWrite", "IORead", "NetworkSend", "NetworkReceive"])


client = docker.DockerClient(base_url='10.0.8.48:2375')
# client2 = docker.APIClient(base_url='127.0.0.1:2375')

containers = client.containers.list()

containerList = []
for con in containers:
    # stats2 = client2.stats(con.name,decode=True,stream=False)
    conStats = con.stats(decode=True,stream=False)
    #print(conStats)

    # var cpuDelta = conStats['cpu_stats']['cpu_usage']['total_usage'] -  conStats['precpu_stats']['cpu_usage']['total_usage']
    # var systemDelta = res.cpu_stats.system_cpu_usage - res.precpu_stats.system_cpu_usage
    # var RESULT_CPU_USAGE = cpuDelta / systemDelta * 100;

    cpu = bytesToMB(conStats['cpu_stats']['cpu_usage']['total_usage'])
    memory = bytesToMB(conStats['memory_stats']['privateworkingset'])
    ioWrite =  bytesToMB(conStats['storage_stats']['write_size_bytes'])
    ioRead =  bytesToMB(conStats['storage_stats']['read_size_bytes'])
    network = get_Dict_Value(conStats['networks'],0)
    networkReceive = bytesToMB(network['rx_bytes'])
    networkSend = bytesToMB(network['tx_bytes'])

    containerList.append(Container(con.id,con.name,con.status,cpu,memory,ioWrite,ioRead,networkReceive,networkSend))

# for con in containerList:
#     c.labels(con.id,con.name,con.status,con.cpu,con.memory,con.ioWrite, con.ioRead,con.networkSend,con.networkReceive).inc()

for con in containerList:
    # jsonData = json.dumps(con, default=jsonDefault)
    # jsonToPython = json.loads(jsonData)
    i = Info('docker_container_'+ con.name, 'Docker container')
    i.info(toJSON(con))


    #jsonString = containerList.toJSON()

    # Create a metric to track time spent and requests made.
    #REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

    # c = Counter('my_failures', 'Description of counter')
    # c.inc()     # Increment by 1
    # c.inc(1.6)  # Increment by given value

    # g = Gauge('my_inprogress_requests', 'Description of gauge')
    # g.inc()      # Increment by 1
    # g.dec(10)    # Decrement by given value
    # g.set(4.2)   # Set to a given value

    # Convert requests and duration to a summary in seconds
    # metric = Metric('containers','Docker container stats.', 'summary')
    # metric.add_sample('svc_requests_duration_seconds_count',value=14324, labels={})
    # metric.add_sample('svc_requests_duration_seconds_sum',value=1235257, labels={})

# Decorate function with metric.
#@REQUEST_TIME.time()
# def process_request(t):
#     """A dummy function that takes some time."""
#     time.sleep(t)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)

    # Generate some requests.
    while True:
        time.sleep(5000)

    # app = make_wsgi_app()
    # httpd = make_server('', 8000, application)
    # httpd.serve_forever()

    # getDockerValues()

    # Create my app
    # app = Flask(__name__)

    # # Add prometheus wsgi middleware to route /metrics requests
    # app_dispatch = DispatcherMiddleware(app, {
    #     '/metrics': getDockerValues()
    # })