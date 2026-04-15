# shot_chart.py

from court_drawing import draw_court

# 各ゾーンの描画位置（3Pはライン外に表示）
zone_coords = {
    "restricted_area": (0, 20),
    "in_paint": (0, 100),
    "mid_range": (0, 195),
    "right_corner": (260, 0),      # ライン外
    "left_corner": (-260, 0),      # ライン外
    "right_wing": (200, 150),       # ライン外
    "left_wing": (-200, 150),       # ライン外
    "top_3": (0, 250),              # アーチ上
}

def draw_shot_chart(player_name, player_data, ax, title=""):
    draw_court(ax)
    stats = player_data.loc[player_name]

    for zone, (x, y) in zone_coords.items():
        if zone in stats:
            value = stats[zone]
            ax.text(x, y, f"{value:.1f}%", ha='center', va='center', fontsize=11, weight='bold')

    ax.set_title(title, fontsize=14)
#-----------------------------------------------------------------------------------------------------
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

# アプリタイトル
st.title(" NBA 類似選手推薦システム")
st.markdown("選手のシュート傾向をもとに、似た選手を可視化して表示します。")

# 選手選択
selected_player = st.selectbox("選手を検索してください", vectors.index)

if selected_player:
    pos = df.loc[selected_player]["position"]
    st.markdown(f"###  入力選手: **{selected_player}**（{pos}）")

    fig, ax = plt.subplots(figsize=(7, 7))
    draw_shot_chart(selected_player, vectors, ax, title=selected_player)
    st.pyplot(fig)

    # 類似選手の推薦（改善済 recommend_similar 使用）
    similar_players = recommend_similar(
        player_name=selected_player,
        vectors=vectors,
        full_df=df,
        top_n=3,
        same_position=True,
        min_shots=200
    )

    st.markdown("###  類似選手")
    cols = st.columns(3)
    for i, (_, row) in enumerate(similar_players.iterrows()):
        with cols[i]:
            st.markdown(f"**{row['player_name']}**（{row['position']}）")
            st.caption(f"試投数: {int(row['total_shots'])} / 成功率: {row['overall']:.1f}% / 類似度: {row['similarity']:.2f}")
            fig_sim, ax_sim = plt.subplots(figsize=(4, 4))
            draw_shot_chart(row["player_name"], vectors, ax_sim, title=row["player_name"])
            st.pyplot(fig_sim)
