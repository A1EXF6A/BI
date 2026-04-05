from fastapi import APIRouter, HTTPException
from typing import Optional
from app.services.clustering_service import ClusteringService

router = APIRouter()


_TABLE_MAP = {
    "factventas": "FactVentas",
    "factinventario": "FactInventario",
    "factdistribucion": "FactDistribucion",
    "factfabricacion": "FactFabricacion",
    "factabastecimiento": "FactAbastecimiento",
    "factventascombo": "FactVentasCombo",
}


@router.get("/clusters/{table}")
def get_clusters(table: str, k: Optional[int] = 3, sample: Optional[int] = 0, limit: Optional[int] = 0, page: Optional[int] = 1):
    key = table.lower()
    if key not in _TABLE_MAP:
        raise HTTPException(status_code=404, detail="Tabla no encontrada")
    collection = _TABLE_MAP[key]
    res = ClusteringService.cluster_table(collection, k, sample=sample, limit=limit, page=page)
    # log result summary
    try:
        import logging
        logger = logging.getLogger("uvicorn")
        if isinstance(res, dict) and 'summaries' in res:
            logger.info(f"Clusters calculated for {collection}: clusters={len(res['summaries'])}")
        else:
            logger.info(f"Clusters response for {collection}: {res}")
    except Exception:
        pass
    return res