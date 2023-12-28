from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class DB_action():
    def __init__(self):

        from dotenv import load_dotenv, find_dotenv
        from os import environ

        load_dotenv(find_dotenv())
        password = environ.get("MONGODB_PWD")
        user = environ.get("MONGODB_USER")
        conn_string = f"mongodb+srv://{user}:{password}@cluster0.vk1gemz.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(conn_string)
        self.db = client.BotDataBase

    def get(self, coll_name: str = None) -> list[str]:
        collection = self.db.Targets if coll_name == "Targets" else self.db.Donors

        result = []
        cursor = collection.find()
        
        for x in cursor:
            result.append(x['channel_id'])
        return result

    def send(self, coll_name, ids: str = None) -> str:
        collection = self.db.Targets if coll_name == "Targets" else self.db.Donors
        ids = set(ids.replace(" ", "").split(","))
        length = 0
        try:
            for id in ids:
                temp = collection.find({'channel_id': f'{id}'})
                id_in_base = [x['channel_id'] for x in temp]

                if id not in id_in_base:
                    collection.insert_one({
                    "channel_id": id})
                    length+=1
            return (f"Successfully added {length} id's to database", ids)

        except Exception as e:
            return e

class Ids():
    tech: int = -1002085744420
    targets: list[int] = DB_action().get("Targets")
    donors: list[int] = DB_action().get("Donors")