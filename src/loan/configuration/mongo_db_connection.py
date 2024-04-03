from src.loan.constant.database import DATABASE_NAME
import os
import pymongo
import certifi

ca = certifi.where()
class MongoDDClient:
    client = None
    
    def __init__(self, database_name= DATABASE_NAME) -> None:
        try:
            if MongoDDClient.client is None:
                mongo_db_url = os.getenv('MONGO_DB_URL')
                MongoDDClient.client = pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
                self.client = MongoDDClient.client
                self.database = self.client[database_name]
                self.database_name = database_name
        except Exception as e:
            raise e