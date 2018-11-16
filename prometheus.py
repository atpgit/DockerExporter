from prometheus_client import start_http_server, Summary, Counter, Metric, Gauge, Info
import time
import docker
import json

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

class list:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class Container() :
    def __init__(self,id,name,status,stats) :
        self.id= id
        self.name= name
        self.status = status
        self.stats = stats

class Stats() :
    def __init__(self,cpu,memory,ioWrite,ioRead,networkReceive,networkSend) :
        self.cpu= cpu
        self.memory= memory
        self.ioWrite = ioWrite
        self.ioRead = ioRead
        self.networkReceive = networkReceive
        self.networkSend = networkSend

client = docker.DockerClient(base_url='127.0.0.1:2375')
# client2 = docker.APIClient(base_url='127.0.0.1:2375')
containers = client.containers.list()

containerList = []
for con in containers:
    #stats = client2.stats(con.name,decode=True)
    conStats = con.stats(decode=True,stream=False)
    #print(conStats)
    cpu = bytesToMB(conStats['cpu_stats']['cpu_usage']['total_usage'])
    memory = bytesToMB(conStats['memory_stats']['privateworkingset'])
    ioWrite =  bytesToMB(conStats['storage_stats']['write_size_bytes'])
    ioRead =  bytesToMB(conStats['storage_stats']['read_size_bytes'])
    network = get_Dict_Value(conStats['networks'],0)
    networkReceive = bytesToMB(network['rx_bytes'])
    networkSend = bytesToMB(network['tx_bytes'])

    stats = Stats(cpu,memory,ioWrite,ioRead,networkReceive,networkSend)

    containerList.append(Container(con.id,con.name,con.status, stats))

c = Counter('docker_containers', 'Container List', ['Id', 'Name', 'Status', "Cpu", "Memory", "IOWrite", "IORead", "NetworkSend", "NetworkReceive"])
for con in containerList:
    c.labels(con.id,con.name,con.status,con.stats.cpu,con.stats.memory,con.stats.ioWrite, con.stats.ioRead,con.stats.networkSend,con.stats.networkReceive).inc()
    
# for con in containerList:
#     print(con.name)

#jsonString = containerList.toJSON()

# jsonData = json.dumps(containerList, default=jsonDefault)

# jsonToPython = json.loads(jsonData)

# Create a metric to track time spent and requests made.
#REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# c = Counter('my_failures', 'Description of counter')
# c.inc()     # Increment by 1
# c.inc(1.6)  # Increment by given value

# g = Gauge('my_inprogress_requests', 'Description of gauge')
# g.inc()      # Increment by 1
# g.dec(10)    # Decrement by given value
# g.set(4.2)   # Set to a given value


# i = Info('docker_containers', 'Docker containers')
# #json = {'version': '1.2.3', 'buildhost': 'foo@bar'}
# i.info(jsonToPython[0])

# Convert requests and duration to a summary in seconds
# metric = Metric('containers','Docker container stats.', 'summary')
# metric.add_sample('svc_requests_duration_seconds_count',value=14324, labels={})
# metric.add_sample('svc_requests_duration_seconds_sum',value=1235257, labels={})

# Decorate function with metric.
#@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        process_request(5000)