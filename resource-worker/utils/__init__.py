import datetime
from io import BytesIO
from zipfile import ZipFile, ZipInfo


def utc_now():
  return datetime.datetime.now(datetime.timezone.utc)

def compress_files(files):
  zip_data = BytesIO()

  with ZipFile(zip_data, 'w') as zip_file:
    for filename, data in files:
      metadata = ZipInfo(filename)
      zip_file.writestr(metadata, data.getvalue())

  zip_data.seek(0)

  return zip_data
