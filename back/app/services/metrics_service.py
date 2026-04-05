from app.repositories.general_repository import GeneralRepository
from app.utils.dataframe_builder import build_dataframe

class MetricsService:

    @staticmethod
    def ventas_metrics():
        data = GeneralRepository.get_collection_data("FactVentas")
        df = build_dataframe(data)

        return {
            "total_ventas": df["IngresoTotal"].sum(),
            "promedio_venta": df["IngresoTotal"].mean(),
            "total_margen": df["MargenNeto"].sum()
        }