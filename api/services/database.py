import pymongo

from models import DeviceDocument


class Database:
  def __init__(self, hostname, port, username, password):
    self.hostname = hostname
    self.port = port
    self.username = username
    self.password = password

    self.client = pymongo.MongoClient(
      self.hostname, int(self.port), username = self.username, password = self.password)
    self.db = self.client['db']

  def find(self, document_id, collection_name):
    collection = self.db[collection_name]
    document = collection.find_one(document_id)

    return DeviceDocument(**document)

  def save(self, document, collection_name):
    collection = self.db[collection_name]
    collection.insert_one(document.dict(by_alias = True))

    return document

  def save_many(self, documents, collection_name):
    collection = self.db[collection_name]
    collection.insertMany([document.dict(by_alias = True) for document in documents])

    return documents
