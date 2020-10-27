import json
import minio


class Storage:
  def __init__(self, domain, secure_domain, hostname, port, access_key, secret_key):
    self.domain = domain
    self.secure_domain = secure_domain
    self.hostname = hostname
    self.port = port
    self.access_key = access_key
    self.secret_key = secret_key

    self.client = minio.Minio(
      f'{self.hostname}:{self.port}', self.access_key, self.secret_key, secure = False)

    bucket_names = ['scenes', 'images']

    for bucket_name in bucket_names:
      if not self.client.bucket_exists(bucket_name):
        policy = {
          'Version': '2012-10-17',
          'Statement': [{
            'Sid': 'PublicReadOnly',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': 's3:GetObject',
            'Resource': f'arn:aws:s3:::{bucket_name}/*'
          }]
        }

        self.client.make_bucket(bucket_name)
        self.client.set_bucket_policy(bucket_name, json.dumps(policy))

  def upload(self, data, metadata, bucket_name, job_id, task_id = None):
    filename = metadata['filename']
    content_type = metadata['content_type']
    content_length = metadata['content_length']

    if task_id is None:
      object_name = f'{job_id}/{filename}'
    else:
      object_name = f'{job_id}/{task_id}/{filename}'

    protocol = 'https' if self.secure_domain else 'http'
    resource_url = f'{protocol}://{self.domain}/{bucket_name}/{object_name}'

    self.client.put_object(bucket_name, object_name, data, content_length, content_type)

    result = {
      'metadata': metadata,
      'resource_url': resource_url
    }

    return result
