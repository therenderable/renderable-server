import os
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

    protocol = 'https' if self.secure_domain else 'http'
    self.base_url = f'{protocol}://{self.domain}'

    self.client = minio.Minio(
      f'{self.hostname}:{self.port}', self.access_key, self.secret_key, secure = False)

    bucket_names = ['scenes', 'images', 'reels']

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

  def upload(self, file, content_type, bucket_name, object_name):
    file_size = os.fstat(file.fileno()).st_size
    resource_url = f'{self.base_url}/{bucket_name}/{object_name}'

    self.client.put_object(bucket_name, object_name, file, file_size, content_type)

    result = {
      'bucket_name': bucket_name,
      'object_name': object_name,
      'resource_url': resource_url
    }

    return result

  def remove(self, bucket_name, object_name):
    resource_url = f'{self.base_url}/{bucket_name}/{object_name}'

    self.client.remove_object(bucket_name, object_name)

    result = {
      'bucket_name': bucket_name,
      'object_name': object_name,
      'resource_url': resource_url
    }

    return result
