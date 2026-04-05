from fastapi import APIRouter
from app.services.clustering_service import ClusteringService

router = APIRouter()

@router.get("/clusters")
def get_clusters():
    return ClusteringService.cluster_productos()