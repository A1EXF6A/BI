import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from app.repositories.general_repository import GeneralRepository
from app.utils.dataframe_builder import build_dataframe

class CollaborativeRecommender:

    @staticmethod
    def recommend(collection_name="FactVentas"):
        data = GeneralRepository.get_collection_data(collection_name)
        df = build_dataframe(data)

        user_item = df.pivot_table(
            index="Cliente.ClienteKey",
            columns="Producto.NombreProducto",
            values="CantidadVendida",
            fill_value=0
        )

        similarity = cosine_similarity(user_item)

        return similarity.tolist()