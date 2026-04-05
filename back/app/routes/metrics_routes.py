from fastapi import APIRouter
from app.services.metrics_service import MetricsService

router = APIRouter()

@router.get("/metrics/ventas")
def get_metrics():
    return MetricsService.ventas_metrics()