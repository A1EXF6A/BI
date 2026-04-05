from fastapi import APIRouter
import logging
from app.services.general_service import GeneralService

logger = logging.getLogger("uvicorn")

router = APIRouter()


def _log_response(path: str, resp):
    try:
        # log a short preview to avoid flooding
        preview = resp
        if isinstance(resp, list):
            preview = resp[:5]
        logger.info(f"Response for {path}: {preview}")
    except Exception as e:
        logger.exception(f"Error logging response for {path}: {e}")


@router.get("/factventas")
def get_fact_ventas():
    res = GeneralService.get_fact_ventas()
    _log_response("/factventas", res)
    return res


@router.get("/factabastecimiento")
def get_fact_abastecimiento():
    res = GeneralService.get_fact_abastecimiento()
    _log_response("/factabastecimiento", res)
    return res


@router.get("/factdistribucion")
def get_fact_distribucion():
    res = GeneralService.get_fact_distribucion()
    _log_response("/factdistribucion", res)
    return res


@router.get("/factfabricacion")
def get_fact_fabricacion():
    res = GeneralService.get_fact_fabricacion()
    _log_response("/factfabricacion", res)
    return res


@router.get("/factinventario")
def get_fact_inventario():
    res = GeneralService.get_fact_inventario()
    _log_response("/factinventario", res)
    return res


@router.get("/factventascombo")
def get_fact_ventas_combo():
    res = GeneralService.get_fact_ventas_combo()
    _log_response("/factventascombo", res)
    return res