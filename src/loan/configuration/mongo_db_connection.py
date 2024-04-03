from src.loan.constant.database import DATABASE_NAME
import os
import pymongo
import certifi

ca = certifi.where()
class MongoDBClient:
    client = None
    
    def __init__(self, database_name= DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = "mongodb+srv://nishantborkar139:swarna12@cluster0.cggllqu.mongodb.net/"
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
                self.client = MongoDBClient.client
                self.database = self.client[database_name]
                self.database_name = database_name
        except Exception as e:
            raise e