from app.repositories.general_repository import GeneralRepository
from app.utils.dataframe_builder import build_dataframe
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import pandas as pd

class InventorySimilarityRecommender:

    @staticmethod
    def recommend(producto_name_or_key, top_n=5, collection_name="FactInventario"):
        """Recommend similar products based on inventory behavior:
        features: StockInicial, StockFinal, VentasPeriodo, Reposiciones (if available)
        Also compute turnover = VentasPeriodo / ((StockInicial+StockFinal)/2 + eps)
        Returns top_n similar products with score and an interpretation label.
        """
        data = GeneralRepository.get_collection_data(collection_name)
        df = build_dataframe(data)
        if df is None or df.empty:
            return {"error": "No hay datos en FactInventario"}

        # normalize product-level (aggregate if multiple rows per product)
        # find product key/name columns
        prod_key_col = None
        prod_name_col = None
        for c in df.columns:
            lc = c.lower()
            if 'productokey' in lc or lc.endswith('productokey') or '.productokey' in lc:
                prod_key_col = c
            if 'nombreproducto' in lc or 'producto.nombre' in lc or 'nombre_producto' in lc:
                prod_name_col = c
        # fallbacks
        if prod_name_col is None:
            # try nested key like Producto.NombreProducto
            prod_name_col = next((c for c in df.columns if 'nombreproducto' in c.lower() or 'producto.nombre' in c.lower()), None)
        if prod_key_col is None:
            prod_key_col = next((c for c in df.columns if 'productokey' in c.lower() or 'product_key' in c.lower()), None)

        # select numeric features if present
        features = []
        for f in ["StockInicial", "StockFinal", "VentasPeriodo", "Reposiciones"]:
            if f in df.columns:
                features.append(f)
            else:
                # try lowercase variants
                found = next((c for c in df.columns if c.lower().endswith(f.lower()) or f.lower() in c.lower()), None)
                if found:
                    features.append(found)
        if not features:
            return {"error": "No se encontraron columnas numéricas para inventario"}

        # aggregate per product
        group_by_col = prod_name_col if prod_name_col in df.columns else prod_key_col if prod_key_col in df.columns else df.columns[0]
        prod_df = df.groupby(group_by_col)[features].mean().reset_index()

        # compute turnover
        si = features[features.index(next((x for x in features if 'StockInicial'.lower() in x.lower()), features[0]))] if any('stockinicial' in c.lower() for c in features) else None
        sf = next((x for x in features if 'stockfinal' in x.lower()), None)
        vp = next((x for x in features if 'ventasperiodo' in x.lower() or 'ventas' in x.lower()), None)
        # add turnover safely
        eps = 1e-6
        if vp is not None and (si is not None or sf is not None):
            prod_df['turnover'] = prod_df[vp] / ((prod_df[si] if si in prod_df.columns else 0 + prod_df[sf] if sf in prod_df.columns else 0)/2 + eps)
            extra_feat = 'turnover'
            feature_cols = [c for c in features if c in prod_df.columns] + [extra_feat]
        else:
            feature_cols = [c for c in features if c in prod_df.columns]

        # prepare matrix
        X = prod_df[feature_cols].fillna(0).values
        scaler = StandardScaler()
        Xs = scaler.fit_transform(X)

        sim = cosine_similarity(Xs)
        sim_df = pd.DataFrame(sim, index=prod_df[group_by_col].astype(str), columns=prod_df[group_by_col].astype(str))

        key = str(producto_name_or_key)
        # try to match by name or key
        if key not in sim_df.index:
            # try to find by key if numeric
            if prod_key_col and any(str(k) == key for k in prod_df[prod_key_col].astype(str)):
                key = next((str(k) for k in prod_df[prod_key_col].astype(str) if str(k) == key), key)
            else:
                # attempt partial match on name
                matches = [idx for idx in sim_df.index if key.lower() in idx.lower()]
                if matches:
                    key = matches[0]
                else:
                    return {"error": "Producto no encontrado en inventario"}

        scores = sim_df[key].sort_values(ascending=False)[1:int(top_n)+1]
        recommendations = []
        # build simple interpretation
        for prod, score in scores.items():
            row = prod_df[prod_df[group_by_col].astype(str) == prod].iloc[0]
            stock_avg = 0
            if 'StockInicial' in prod_df.columns and 'StockFinal' in prod_df.columns:
                stock_avg = (row.get('StockInicial', 0) + row.get('StockFinal', 0))/2
            ventas = row.get(vp, 0) if vp in row.index else 0
            if stock_avg > 0 and ventas/ (stock_avg + eps) < 0.2:
                interp = 'Alto stock y baja venta'
            elif ventas/ (stock_avg + eps) > 1:
                interp = 'Alta rotación'
            else:
                interp = 'Rotación moderada'
            recommendations.append({"producto": prod, "score": float(score), "interpretation": interp})

        return {"recommendations": recommendations}
