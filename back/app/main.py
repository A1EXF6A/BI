from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import metrics_routes, clustering_routes, recommendation_routes

app = FastAPI()

# 🔥 CORS (ANTES de las rutas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# rutas
app.include_router(metrics_routes.router)
app.include_router(clustering_routes.router)
app.include_router(recommendation_routes.router)    