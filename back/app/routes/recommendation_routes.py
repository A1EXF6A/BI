from fastapi import APIRouter
from app.services.recommendation.similarity import SimilarityRecommender

router = APIRouter()

@router.get("/recommend/similarity/{producto}")
def recommend(producto: str):
    return SimilarityRecommender.recommend(producto)