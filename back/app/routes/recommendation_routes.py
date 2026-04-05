from fastapi import APIRouter, Query
from app.services.recommendation.similarity import SimilarityRecommender
from app.services.recommendation.collaborative import CollaborativeRecommender
from app.services.recommendation.content_based import ContentBasedRecommender

router = APIRouter()


@router.get("/recommend/similarity/{producto}")
def recommend_similarity(producto: str):
    return SimilarityRecommender.recommend(producto)


@router.get("/recommend/collaborative/{cliente_key}")
def recommend_collaborative(cliente_key: int, n: int = Query(5, ge=1)):
    return CollaborativeRecommender.recommend_for_client(cliente_key, top_n=n)


@router.get("/recommend/content/{producto}")
def recommend_content(producto: str, n: int = Query(5, ge=1)):
    return ContentBasedRecommender.recommend(producto, top_n=n)


from app.services.recommendation.inventory_similarity import InventorySimilarityRecommender


@router.get("/recommend/inventory/similarity/{producto}")
def recommend_inventory_similarity(producto: str, n: int = Query(5, ge=1)):
    return InventorySimilarityRecommender.recommend(producto, top_n=n)