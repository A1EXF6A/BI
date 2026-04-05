from app.repositories.general_repository import GeneralRepository
from app.utils.dataframe_builder import build_dataframe
import logging
import numpy as np
import pandas as pd

logger = logging.getLogger("uvicorn")


def _to_native(v):
    try:
        if v is None:
            return None
        if isinstance(v, (np.generic,)):
            return v.item()
        if isinstance(v, (np.ndarray,)):
            return v.tolist()
        if isinstance(v, pd.Timestamp):
            return v.isoformat()
        # pandas NA
        if pd.isna(v):
            return None
        return v
    except Exception:
        return v


class MetricsService:

    @staticmethod
    def calculate_metrics(collection_name):
        data = GeneralRepository.get_collection_data(collection_name)
        df = build_dataframe(data)

        # Depuración: Verificar los datos y el DataFrame
        logger.info(f"DataFrame para {collection_name}: {df.shape} rows, columns: {list(df.columns)[:10]}")

        def mk(d):
            return {k: _to_native(v) for k, v in d.items()}

        if collection_name == "FactAbastecimiento":
            res = {
                "total_costo_compra": df["CostoTotalCompra"].sum() if "CostoTotalCompra" in df else None,
                "promedio_tiempo_entrega": df["TiempoEntregaDias"].mean() if "TiempoEntregaDias" in df else None,
            }
            return mk(res)

        elif collection_name == "FactDistribucion":
            res = {
                "total_costo_envio": df["CostoEnvioTotal"].sum() if "CostoEnvioTotal" in df else None,
                "promedio_tiempo_entrega": df["TiempoEntregaPromedio"].mean() if "TiempoEntregaPromedio" in df else None,
            }
            return mk(res)

        elif collection_name == "FactFabricacion":
            res = {
                "total_costo_fabricacion": df["CostoFabricacion"].sum() if "CostoFabricacion" in df else None,
                "promedio_unidades_fabricadas": df["UnidadesFabricadas"].mean() if "UnidadesFabricadas" in df else None,
            }
            return mk(res)

        elif collection_name == "FactInventario":
            res = {
                "stock_inicial_total": df["StockInicial"].sum() if "StockInicial" in df else None,
                "stock_final_total": df["StockFinal"].sum() if "StockFinal" in df else None,
            }
            return mk(res)

        elif collection_name == "FactVentas":
            res = {
                "total_ventas": df["IngresoTotal"].sum() if "IngresoTotal" in df else None,
                "promedio_venta": df["IngresoTotal"].mean() if "IngresoTotal" in df else None,
                "total_margen": df["MargenNeto"].sum() if "MargenNeto" in df else None,
            }
            return mk(res)

        elif collection_name == "FactVentasCombo":
            res = {
                "total_ingreso_combos": df["IngresoTotal"].sum() if "IngresoTotal" in df else None,
                "promedio_margen_combos": df["MargenNeto"].mean() if "MargenNeto" in df else None,
            }
            return mk(res)

        else:
            return {"error": "Tabla no reconocida"}