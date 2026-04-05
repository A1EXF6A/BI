from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from app.repositories.general_repository import GeneralRepository
from app.utils.dataframe_builder import build_dataframe
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger("uvicorn")


class ClusteringService:

    @staticmethod
    def _select_features_for_table(df: pd.DataFrame, table: str):
        # return list of columns to use for clustering (numerical)
        mapping = {
            "FactVentas": ["IngresoTotal", "MargenNeto", "CantidadVendida"],
            "FactInventario": ["StockInicial", "StockFinal", "VentasPeriodo", "Reposiciones"],
            "FactDistribucion": ["CostoEnvioTotal", "TiempoEntregaPromedio", "PedidosDespachados"],
            "FactFabricacion": ["CostoFabricacion", "UnidadesFabricadas", "NumeroComponentes"],
            "FactAbastecimiento": ["CantidadComprada", "CostoTotalCompra", "TiempoEntregaDias"],
            "FactVentasCombo": ["IngresoTotal", "MargenNeto", "CantidadProducto1", "CantidadProducto2"],
        }
        cols = mapping.get(table, [])
        return [c for c in cols if c in df.columns]

    @staticmethod
    def _interpret_clusters(df: pd.DataFrame, features: list, table: str):
        # Basic heuristics: describe cluster by highest/lowest means per feature
        interpretations = {}
        grouped = df.groupby('cluster')
        means = grouped[features].mean()
        for cluster_label, row in means.iterrows():
            parts = []
            for feature in features:
                val = row.get(feature, 0)
                overall = df[feature].mean() if feature in df.columns else 0
                if overall == 0:
                    parts.append(f"medio {feature}")
                    continue
                if val >= overall * 1.2:
                    parts.append(f"alto {feature}")
                elif val <= overall * 0.8:
                    parts.append(f"bajo {feature}")
                else:
                    parts.append(f"medio {feature}")
            # join parts and map to business-friendly label
            label = ", ".join(parts)
            # map to concise interpretation for known tables
            if table == "FactVentas":
                if any('alto IngresoTotal'.lower() in p.lower() for p in parts) or any('alto MargenNeto'.lower() in p.lower() for p in parts):
                    biz = "Alto valor"
                elif any('bajo IngresoTotal'.lower() in p.lower() for p in parts):
                    biz = "Bajo valor"
                else:
                    biz = "Valor medio"
            elif table == "FactInventario":
                if any('bajo StockFinal'.lower() in p.lower() for p in parts) or any('bajo StockInicial'.lower() in p.lower() for p in parts):
                    biz = "Bajo stock"
                elif any('alto StockFinal'.lower() in p.lower() for p in parts):
                    biz = "Sobre stock"
                else:
                    biz = "Stock óptimo"
            else:
                biz = label

            interpretations[int(cluster_label)] = biz
        return interpretations

    @staticmethod
    def cluster_table(table: str, k: int = 3, sample: int = 0, limit: int = 0, page: int = 1):
        data = GeneralRepository.get_collection_data(table)
        if not data:
            return {"error": "No hay datos"}

        df = build_dataframe(data)

        logger.info(f"Clustering request: table={table}, rows={len(df)}")

        # select numeric features
        features = ClusteringService._select_features_for_table(df, table)
        logger.info(f"Selected features for {table}: {features}")
        if not features:
            return {"error": "No hay features numéricos para clustering"}

        # fill missing numeric values
        for f in features:
            df[f] = pd.to_numeric(df.get(f, 0), errors='coerce').fillna(0)

        X = df[features].values

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        model = KMeans(n_clusters=k, random_state=42)
        labels = model.fit_predict(X_scaled)
        df['cluster'] = labels

        # log centers and counts
        try:
            centers = model.cluster_centers_.tolist()
            counts = {int(l): int((labels == l).sum()) for l in np.unique(labels)}
            logger.info(f"KMeans centers: {centers}")
            logger.info(f"Cluster counts: {counts}")
        except Exception as e:
            logger.exception(f"Error logging cluster internals: {e}")

        # interpretation
        interpretations = ClusteringService._interpret_clusters(df, features, table)

        # prepare records to return: include key fields plus cluster
        key_fields = []
        for candidate in ["Producto.NombreProducto", "Producto.ProductoKey", "VentaKey", "InventarioKey", "DistribucionKey", "FabricacionKey", "AbastecimientoKey", "VentaComboKey"]:
            if candidate in df.columns:
                key_fields.append(candidate)
        # optionally reduce the returned records payload (compute clusters on full df, but return sample/page)
        records = []
        df_to_return = df
        try:
            if sample and int(sample) > 0:
                n = min(int(sample), len(df))
                df_to_return = df.sample(n=n, random_state=42)
            elif limit and int(limit) > 0:
                p = max(int(page), 1)
                start = (p - 1) * int(limit)
                df_to_return = df.iloc[start:start + int(limit)]
        except Exception:
            df_to_return = df

        for _, row in df_to_return.iterrows():
            rec = {f: (row[f] if f in row.index else None) for f in key_fields}
            for f in features:
                rec[f] = _to_native(row[f])
            rec['cluster'] = int(row['cluster'])
            rec['interpretation'] = interpretations.get(int(row['cluster']), "")
            records.append(rec)

        summaries = {}
        counts = {}
        grouped = df.groupby('cluster')
        for c, g in grouped:
            summaries[int(c)] = {f: _to_native(g[f].mean()) for f in features}
            counts[int(c)] = int(len(g))

        # log summary preview
        try:
            logger.info(f"Cluster summaries (first 5 records): {records[:5]}")
        except Exception:
            pass

        return {"records": records, "summaries": summaries, "interpretations": interpretations, "counts": counts}


def _to_native(v):
    try:
        if pd.isna(v):
            return None
    except Exception:
        pass
    if isinstance(v, (np.generic,)):
        return v.item()
    if isinstance(v, (np.ndarray,)):
        return v.tolist()
    return v