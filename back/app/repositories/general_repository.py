from app.config.database import get_collection

class GeneralRepository:

    @staticmethod
    def get_collection_data(collection_name):
        collection = get_collection(collection_name)
        return list(collection.find({}, {"_id": 0}))