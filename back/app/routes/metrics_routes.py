from fastapi import APIRouter, HTTPException
import logging
from app.services.metrics_service import MetricsService

router = APIRouter()
logger = logging.getLogger("uvicorn")

# mapping from frontend path (lowercase) to collection names used in MetricsService
_TABLE_MAP = {
    "factventas": "FactVentas",
    "factabastecimiento": "FactAbastecimiento",
    "factdistribucion": "FactDistribucion",
    "factfabricacion": "FactFabricacion",
    "factinventario": "FactInventario",
    "factventascombo": "FactVentasCombo",
}


@router.get("/metrics/{table}")
def get_metrics(table: str):
    key = table.lower()
    if key not in _TABLE_MAP:
        raise HTTPException(status_code=404, detail="Tabla de hechos no encontrada")

    collection_name = _TABLE_MAP[key]
    res = MetricsService.calculate_metrics(collection_name)
    logger.info(f"Metrics for {collection_name}: {res}")
    return res