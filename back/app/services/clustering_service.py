from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from app.repositories.general_repository import GeneralRepository
from app.utils.dataframe_builder import build_dataframe

class ClusteringService:

    @staticmethod
    def cluster_productos(k=3):
        data = GeneralRepository.get_collection_data("FactVentas")
        df = build_dataframe(data)

        X = df[[
            "CantidadVendida",
            "PrecioFinal",
            "MargenNeto"
        ]]

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        model = KMeans(n_clusters=k, random_state=42)
        df["cluster"] = model.fit_predict(X_scaled)

        return df[[
            "Producto.NombreProducto",
            "cluster"
        ]].to_dict(orient="records")