from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.repositories.general_repository import GeneralRepository
from app.utils.dataframe_builder import build_dataframe

class ContentBasedRecommender:

    @staticmethod
    def recommend(producto_nombre, collection_name="FactVentas"):
        data = GeneralRepository.get_collection_data(collection_name)
        df = build_dataframe(data)

        df["features"] = (
            df["Producto.Categoria"] + " " +
            df["Producto.Subcategoria"] + " " +
            df["Producto.TipoProducto"]
        )

        vectorizer = TfidfVectorizer()
        matrix = vectorizer.fit_transform(df["features"])

        sim = cosine_similarity(matrix)

        index = df[df["Producto.NombreProducto"] == producto_nombre].index[0]

        scores = list(enumerate(sim[index]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)

        return [
            df.iloc[i[0]]["Producto.NombreProducto"]
            for i in scores[1:6]
        ]