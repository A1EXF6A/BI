from sklearn.metrics.pairwise import cosine_similarity
from app.repositories.general_repository import GeneralRepository
from app.utils.dataframe_builder import build_dataframe
import pandas as pd

class SimilarityRecommender:

    @staticmethod
    def recommend(producto_nombre, collection_name="FactVentas"):
        data = GeneralRepository.get_collection_data(collection_name)
        df = build_dataframe(data)

        pivot = df.pivot_table(
            index="Producto.NombreProducto",
            values="IngresoTotal",
            aggfunc="sum"
        )

        sim = cosine_similarity(pivot)

        sim_df = pd.DataFrame(sim, index=pivot.index, columns=pivot.index)

        return sim_df[producto_nombre].sort_values(ascending=False)[1:6].to_dict()