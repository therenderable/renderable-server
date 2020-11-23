import docker


class Autoscaler:
  def __init__(self, hostname, port, certificate_path, average_tasks_per_worker, autoscale_threshold):
    self.hostname = hostname
    self.port = port
    self.certificate_path = certificate_path
    self.average_tasks_per_worker = average_tasks_per_worker
    self.autoscale_threshold = autoscale_threshold

    public_certificate_path = str(self.certificate_path / 'cert.pem')
    private_certificate_path = str(self.certificate_path / 'key.pem')

    tls_config = docker.tls.TLSConfig(
      client_cert = (public_certificate_path, private_certificate_path))

    self.client = docker.DockerClient(f'https://{self.hostname}:{self.port}', tls = tls_config)

  def get_compute_capability(self):
    def filter_by_ready_status(node):
      return node.attrs['Status']['State'] == 'ready'

    nodes = self.client.nodes.list(filters = {'role': 'worker'})
    nodes = list(filter(filter_by_ready_status, nodes))

    return len(nodes) * self.average_tasks_per_worker

  def get_cluster_state(self):
    def format_service(service):
      name = service.attrs['Spec']['Name']
      replicas = service.attrs['Spec']['Mode']['Replicated']['Replicas']

      return name, replicas

    return dict(format_service(service) for service in self.client.services.list())

  def scale_service(self, container_name, replicas):
    service = self.client.services.get(container_name)
    service.scale(replicas)

  def scale(self, task_state):
    import logging

    try:
      def normalize(state):
        total_count = sum(state.values())
        scale_factor = 1 / total_count if total_count > 0 else 0

        return {container_name: count * scale_factor for container_name, count in state.items()}

      def distance(state, target_state):
        return {container_name: target_state[container_name] - factor for container_name, factor in state.items()}=

      task_state = normalize(task_state)

      cluster_state = normalize(self.get_cluster_state())
      target_state = {container_name: task_state.get(container_name, 0) for container_name in cluster_state.keys()}

      error_state = distance(cluster_state, target_state)

      capability = self.get_compute_capability()

      for container_name, error in error_state.items():
        squared_error = error * error

        if squared_error > self.autoscale_threshold * self.autoscale_threshold:
          self.scale_service(container_name, capability * int(max(target_state[container_name], 1)))


    except Exception as e:
      logging.error(e)
