from app.config.database import get_collection

class InventarioRepository:

    @staticmethod
    def get_all():
        collection = get_collection("FactInventario")
        return list(collection.find({}, {"_id": 0}))

    @staticmethod
    def get_by_key(inventario_key):
        collection = get_collection("FactInventario")
        return collection.find_one({"InventarioKey": inventario_key}, {"_id": 0})