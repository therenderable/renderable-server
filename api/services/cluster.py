from enum import Enum

import docker


class ClusterStatus(int, Enum):
  node_already_initialized = 503
  secret_already_exists = 409


class Cluster:
  def __init__(self,
      domain_ip, hostname, port, manager_port, certificate_path,
      registry_domain, secure_registry_domain, registry_username, registry_password, secrets):
    self.domain_ip = domain_ip
    self.hostname = hostname
    self.port = port
    self.manager_port = manager_port
    self.certificate_path = certificate_path
    self.registry_domain = registry_domain
    self.secure_registry_domain = secure_registry_domain
    self.registry_username = registry_username
    self.registry_password = registry_password
    self.secrets = secrets

    public_certificate_path = str(self.certificate_path / 'cert.pem')
    private_certificate_path = str(self.certificate_path / 'key.pem')

    tls_config = docker.tls.TLSConfig(
      client_cert = (public_certificate_path, private_certificate_path))

    self.client = docker.DockerClient(f'https://{self.hostname}:{self.port}', tls = tls_config)

    self._initialize()
    self._login_registry()
    self._register_secrets()

  def _initialize(self):
    try:
      self.client.swarm.init(
        advertise_addr = self.domain_ip, listen_addr = f'0.0.0.0:{self.manager_port}')
    except docker.errors.APIError as error:
      if error.status_code != ClusterStatus.node_already_initialized:
        raise error

  def _login_registry(self):
    protocol = 'https' if self.secure_registry_domain else 'http'
    registry_url = f'{protocol}://{self.registry_domain}/v2/'

    self.client.login(self.registry_username, self.registry_password, registry = registry_url)

  def _register_secrets(self):
    try:
      for name, data in self.secrets.items():
        secret = {
          'name': name.lower(),
          'data': data.encode('utf-8')
        }

        self.client.secrets.create(**secret)
    except docker.errors.APIError as error:
      if error.status_code != ClusterStatus.secret_already_exists:
        raise error

  def join(self, device):
    node_type = device['node_type'].capitalize()

    self.client.swarm.reload()
    return self.client.swarm.attrs['JoinTokens'][node_type]
