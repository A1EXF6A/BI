from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.repositories.general_repository import GeneralRepository
from app.utils.dataframe_builder import build_dataframe

class ContentBasedRecommender:

    @staticmethod
    def recommend(producto_nombre, top_n=5, collection_name="FactVentas"):
        data = GeneralRepository.get_collection_data(collection_name)
        df = build_dataframe(data)

        # build product-level features (unique products)
        prod_df = df.drop_duplicates(subset=["Producto.NombreProducto"]).copy()
        prod_df["features"] = (
            prod_df.get("Producto.Categoria", "") + " " +
            prod_df.get("Producto.Subcategoria", "") + " " +
            prod_df.get("Producto.Marca", "") + " " +
            prod_df.get("Producto.TipoProducto", "")
        )

        vectorizer = TfidfVectorizer()
        matrix = vectorizer.fit_transform(prod_df["features"].fillna(''))

        sim = cosine_similarity(matrix)

        matches = prod_df[prod_df["Producto.NombreProducto"] == producto_nombre]
        if matches.empty:
            return {"error": "Producto no encontrado en datos"}
        index = matches.index[0]

        scores = list(enumerate(sim[index]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)

        result = []
        for i, score in scores[1:int(top_n)+1]:
            result.append({"producto": prod_df.iloc[i]["Producto.NombreProducto"], "score": float(score)})
        return {"recommendations": result}