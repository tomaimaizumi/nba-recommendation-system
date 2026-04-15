# recommend.py

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler,StandardScaler,Normalizer

def load_vectors(csv_path):
    df = pd.read_csv(csv_path)
    df = df.set_index("player_name")
    exclude = ["overall", "total_shots", "made_shots"]
    zone_cols = [col for col in df.columns if col not in exclude]
    return df[zone_cols]

def recommend_similar(player_name, vectors, full_df, top_n=6, same_position=True, min_shots=50):
    # 類似度計算前に正規化 → スケール差で差が見える
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(vectors)
    scaled_df = pd.DataFrame(scaled, index=vectors.index, columns=vectors.columns)

    similarity = cosine_similarity(scaled_df)
    sim_df = pd.DataFrame(similarity, index=scaled_df.index, columns=scaled_df.index)

    # 入力選手以外のスコア
    sim_scores = sim_df[player_name].drop(player_name)

    # 絞り込み
    filtered_df = full_df.copy()
    if same_position:
        pos = full_df.loc[player_name, "position"]
        filtered_df = filtered_df[filtered_df["position"] == pos]
    if min_shots > 0:
        filtered_df = filtered_df[filtered_df["total_shots"] >= min_shots]
    sim_scores = sim_scores[sim_scores.index.isin(filtered_df.index)]

    # 上位N
    top_matches = sim_scores.sort_values(ascending=False).head(top_n)

    result = full_df.loc[top_matches.index].copy()
    result["similarity"] = top_matches.values
    result["player_name"] = result.index

    return result.reset_index(drop=True)
