from io import BytesIO
from docker import APIClient
dockerfile = '''
FROM microsoft/dotnet-framework:4.7.1-windowsservercore-1709
ADD . /app
WORKDIR /app
ENTRYPOINT ["cmd.exe", "/k", "DockerAutonomProject.exe"]
'''
f = BytesIO(dockerfile.encode('utf-8'))
cli = APIClient(base_url='tcp://127.0.0.1:2375')
response = [line for line in cli.build(fileobj=f, rm=True, tag='baseareaimage')]
print(response)