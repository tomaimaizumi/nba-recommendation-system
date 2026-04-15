# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from recommend import load_vectors, recommend_similar
from shot_chart import draw_shot_chart

# データ読み込み
df = pd.read_csv("nba_zone_accuracy_summary.csv")
df = df.set_index("player_name")
vectors = df.drop(columns=["overall", "total_shots", "made_shots", "position"])

# UI
st.title("NBA 類似選手推薦システム")
st.caption("選手のシュート傾向から類似するプレイヤーを推薦し、可視化します。")

# 選手選択
selected_player = st.selectbox("選手を検索してください", vectors.index)

if selected_player:
    pos = df.loc[selected_player]["position"]
    st.markdown(f"### 入力選手: **{selected_player}**（{pos}）")

    fig, ax = plt.subplots(figsize=(7, 7))
    draw_shot_chart(selected_player, vectors, ax, title=selected_player)
    st.pyplot(fig)

    # 類似推薦（正規化＋フィルタ付き）
    similar_players = recommend_similar(
        player_name=selected_player,
        vectors=vectors,
        full_df=df,
        top_n=6,
        same_position=True,
        min_shots=200
    )

    st.markdown("### 類似選手")
    for row_index in range(0, 6, 3):
        cols = st.columns(3)
        for i in range(3):
            player_idx = row_index + i
            if player_idx < len(similar_players):
                row = similar_players.iloc[player_idx]
                with cols[i]:
                    st.markdown(f"### 推薦度第 **{row_index+(i+1)}** 位")
                    name = row["player_name"]
                    pos_sim = row["position"]
                    sim = row["similarity"]
                    st.markdown(f"**{name}**（{pos_sim}）<br>類似度: {sim:.3f}", unsafe_allow_html=True)
                    fig_sim, ax_sim = plt.subplots(figsize=(4, 4))
                    draw_shot_chart(name, vectors, ax_sim, title=name)
                    st.pyplot(fig_sim)
