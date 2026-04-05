import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from app.repositories.general_repository import GeneralRepository
from app.utils.dataframe_builder import build_dataframe

class CollaborativeRecommender:

    @staticmethod
    def recommend_for_client(cliente_key, top_n=10, collection_name="FactVentas"):
        """
        Item-based collaborative filtering recommendations for a given cliente_key.
        Returns top_n product recommendations with scores.
        """
        data = GeneralRepository.get_collection_data(collection_name)
        df = build_dataframe(data)

        # build item-user matrix (items as rows)
        pivot = df.pivot_table(
            index="Producto.NombreProducto",
            columns="Cliente.ClienteKey",
            values="CantidadVendida",
            aggfunc='sum',
            fill_value=0
        )

        # item-item similarity
        item_sim = cosine_similarity(pivot.fillna(0))
        items = pivot.index.to_list()
        sim_df = pd.DataFrame(item_sim, index=items, columns=items)

        # products bought by the client
        client_purchases = df[df["Cliente.ClienteKey"] == cliente_key].groupby("Producto.NombreProducto")["CantidadVendida"].sum()
        if client_purchases.empty:
            return {"error": "Cliente sin compras registradas"}

        scores = {}
        for prod, qty in client_purchases.items():
            if prod not in sim_df.index:
                continue
            sims = sim_df[prod]
            # weighted score by purchase quantity
            for other, s in sims.items():
                if other in client_purchases.index:
                    continue
                scores[other] = scores.get(other, 0) + s * float(qty)

        # normalize and sort
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return {p: float(score) for p, score in ranked[:int(top_n)]}