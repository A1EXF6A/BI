import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class CollaborativeRecommender:

    @staticmethod
    def recommend(df):
        user_item = df.pivot_table(
            index="Cliente.ClienteKey",
            columns="Producto.NombreProducto",
            values="CantidadVendida",
            fill_value=0
        )

        similarity = cosine_similarity(user_item)

        return similarity.tolist()