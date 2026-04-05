from app.repositories.general_repository import GeneralRepository

class GeneralService:

    @staticmethod
    def get_fact_abastecimiento():
        return GeneralRepository.get_fact_abastecimiento()

    @staticmethod
    def get_fact_distribucion():
        return GeneralRepository.get_fact_distribucion()

    @staticmethod
    def get_fact_fabricacion():
        return GeneralRepository.get_fact_fabricacion()

    @staticmethod
    def get_fact_inventario():
        return GeneralRepository.get_fact_inventario()

    @staticmethod
    def get_fact_ventas():
        return GeneralRepository.get_fact_ventas()

    @staticmethod
    def get_fact_ventas_combo():
        return GeneralRepository.get_fact_ventas_combo()