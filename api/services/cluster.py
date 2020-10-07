import docker


class Cluster:
  def __init__(self, domain, hostname, port, master_port):
    self.domain = domain
    self.hostname = hostname
    self.port = port

    self.client = docker.DockerClient(f'tcp://{self.hostname}:{self.port}')

    self.client.swarm.init(
      advertise_addr = self.domain, listen_addr = f'0.0.0.0:{self.master_port}')
