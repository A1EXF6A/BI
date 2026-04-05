from app.config.database import get_collection

class VentasRepository:

    @staticmethod
    def get_all():
        collection = get_collection("FactVentas")
        return list(collection.find({}, {"_id": 0}))

    @staticmethod
    def get_by_key(venta_key):
        collection = get_collection("FactVentas")
        return collection.find_one({"VentaKey": venta_key}, {"_id": 0})