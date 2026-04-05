from app.config.database import get_collection

class GeneralRepository:

    @staticmethod
    def get_collection_data(collection_name):
        collection = get_collection(collection_name)
        return list(collection.find({}, {"_id": 0}))

    @staticmethod
    def get_fact_abastecimiento():
        return GeneralRepository.get_collection_data("FactAbastecimiento")

    @staticmethod
    def get_fact_distribucion():
        return GeneralRepository.get_collection_data("FactDistribucion")

    @staticmethod
    def get_fact_fabricacion():
        return GeneralRepository.get_collection_data("FactFabricacion")

    @staticmethod
    def get_fact_inventario():
        return GeneralRepository.get_collection_data("FactInventario")

    @staticmethod
    def get_fact_ventas():
        return GeneralRepository.get_collection_data("FactVentas")

    @staticmethod
    def get_fact_ventas_combo():
        return GeneralRepository.get_collection_data("FactVentasCombo")